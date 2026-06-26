import express from "express";
import dotenv from "dotenv";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Configuration, PlaidApi, PlaidEnvironments } from "plaid";
import { classifyTransaction, csvEscape, merchantGroup, parseCsvLine, summarizeClassifications } from "./lib/classifier.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
dotenv.config({ path: path.join(__dirname, ".env.local") });

const dataDir = path.join(__dirname, "data");
const itemsPath = path.join(dataDir, "items.json");
const txPath = path.join(dataDir, "transactions.json");
const overridesPath = path.join(__dirname, "overrides.csv");

const port = Number(process.env.PORT || 3333);
const envName = process.env.PLAID_ENV || "production";
const products = (process.env.PLAID_PRODUCTS || "transactions").split(",").map((item) => item.trim());
const countryCodes = (process.env.PLAID_COUNTRY_CODES || "US").split(",").map((item) => item.trim());

if (!process.env.PLAID_CLIENT_ID || !process.env.PLAID_SECRET) {
  console.error("Missing PLAID_CLIENT_ID or PLAID_SECRET in .env.local");
  process.exit(1);
}

if (!PlaidEnvironments[envName]) {
  console.error(`Invalid PLAID_ENV: ${envName}`);
  process.exit(1);
}

const plaid = new PlaidApi(
  new Configuration({
    basePath: PlaidEnvironments[envName],
    baseOptions: {
      headers: {
        "PLAID-CLIENT-ID": process.env.PLAID_CLIENT_ID,
        "PLAID-SECRET": process.env.PLAID_SECRET
      }
    }
  })
);

const app = express();
app.use(express.json({ limit: "1mb" }));
app.use(express.static(path.join(__dirname, "public")));

async function readJson(filePath, fallback) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    if (error.code === "ENOENT") return fallback;
    throw error;
  }
}

async function writeJson(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

async function getItems() {
  return readJson(itemsPath, []);
}

async function setItems(items) {
  await writeJson(itemsPath, items);
}

async function readOverrides() {
  try {
    const text = await fs.readFile(overridesPath, "utf8");
    const lines = text.split(/\r?\n/).filter((line) => line.trim() && !line.startsWith("#"));
    const [headerLine, ...rows] = lines;
    if (!headerLine) return new Map();
    const headers = parseCsvLine(headerLine);
    const map = new Map();
    for (const line of rows) {
      const values = parseCsvLine(line);
      const record = Object.fromEntries(headers.map((header, index) => [header, values[index] || ""]));
      if (record.transaction_id && record.status) {
        map.set(record.transaction_id, record);
      }
    }
    return map;
  } catch (error) {
    if (error.code === "ENOENT") return new Map();
    throw error;
  }
}

async function writeOverrides(overrides) {
  const rows = [
    "transaction_id,status,mindshare_category,note",
    ...[...overrides.values()].map((record) =>
      [record.transaction_id, record.status, record.mindshare_category, record.note || ""].map(csvEscape).join(",")
    )
  ];
  await fs.writeFile(overridesPath, `${rows.join("\n")}\n`);
}

async function classifyAll() {
  const transactions = await readJson(txPath, []);
  const overrides = await readOverrides();
  const rows = transactions
    .map((tx) => classifyTransaction(tx, overrides))
    .sort((a, b) => b.date.localeCompare(a.date) || a.merchant.localeCompare(b.merchant));
  return { rows, summary: summarizeClassifications(rows) };
}

app.post("/api/link-token", async (_req, res, next) => {
  try {
    const request = {
      user: { client_user_id: "scott-internal-test" },
      client_name: "Mindshare Internal Finance",
      products,
      country_codes: countryCodes,
      language: "en"
    };

    if (process.env.PLAID_REDIRECT_URI) {
      request.redirect_uri = process.env.PLAID_REDIRECT_URI;
    }

    const response = await plaid.linkTokenCreate(request);
    res.json({ link_token: response.data.link_token });
  } catch (error) {
    next(error);
  }
});

app.post("/api/exchange-public-token", async (req, res, next) => {
  try {
    const { public_token, institution } = req.body;
    if (!public_token) {
      res.status(400).json({ error: "Missing public_token" });
      return;
    }

    const response = await plaid.itemPublicTokenExchange({ public_token });
    const accessToken = response.data.access_token;
    const itemId = response.data.item_id;
    const items = await getItems();
    items.push({
      item_id: itemId,
      access_token: accessToken,
      institution: institution?.name || "Unknown institution",
      cursor: null,
      created_at: new Date().toISOString()
    });
    await setItems(items);
    res.json({ ok: true, item_id: itemId });
  } catch (error) {
    next(error);
  }
});

app.get("/api/items", async (_req, res, next) => {
  try {
    const items = await getItems();
    res.json({
      items: items.map(({ access_token, ...item }) => item)
    });
  } catch (error) {
    next(error);
  }
});

app.post("/api/sync", async (_req, res, next) => {
  try {
    const items = await getItems();
    const allTransactions = await readJson(txPath, []);
    const byTransactionId = new Map(allTransactions.map((tx) => [tx.transaction_id, tx]));
    const results = [];

    for (const item of items) {
      let cursor = item.cursor;
      let hasMore = true;
      let addedCount = 0;
      let modifiedCount = 0;
      let removedCount = 0;

      while (hasMore) {
        const response = await plaid.transactionsSync({
          access_token: item.access_token,
          cursor,
          count: 500
        });

        for (const tx of response.data.added) {
          byTransactionId.set(tx.transaction_id, {
            ...tx,
            mindshare_source_institution: item.institution,
            mindshare_item_id: item.item_id
          });
          addedCount += 1;
        }

        for (const tx of response.data.modified) {
          byTransactionId.set(tx.transaction_id, {
            ...tx,
            mindshare_source_institution: item.institution,
            mindshare_item_id: item.item_id
          });
          modifiedCount += 1;
        }

        for (const tx of response.data.removed) {
          byTransactionId.delete(tx.transaction_id);
          removedCount += 1;
        }

        cursor = response.data.next_cursor;
        hasMore = response.data.has_more;
      }

      item.cursor = cursor;
      item.last_synced_at = new Date().toISOString();
      results.push({
        item_id: item.item_id,
        institution: item.institution,
        added: addedCount,
        modified: modifiedCount,
        removed: removedCount
      });
    }

    await setItems(items);
    const transactions = [...byTransactionId.values()].sort((a, b) => String(b.date).localeCompare(String(a.date)));
    await writeJson(txPath, transactions);

    res.json({ ok: true, results, transaction_count: transactions.length });
  } catch (error) {
    next(error);
  }
});

app.get("/api/transactions", async (_req, res, next) => {
  try {
    const transactions = await readJson(txPath, []);
    res.json({ transactions });
  } catch (error) {
    next(error);
  }
});

app.get("/api/classifications", async (req, res, next) => {
  try {
    const { rows, summary } = await classifyAll();
    const status = String(req.query.status || "all");
    const q = String(req.query.q || "").trim().toLowerCase();
    let filtered = rows;

    if (status !== "all") {
      filtered = filtered.filter((row) => row.status === status);
    }

    if (q) {
      filtered = filtered.filter((row) =>
        [row.merchant, row.name, row.source, row.plaid_primary, row.plaid_detailed, row.mindshare_category, row.reason]
          .join(" ")
          .toLowerCase()
          .includes(q)
      );
    }

    res.json({ summary, rows: filtered.slice(0, 500) });
  } catch (error) {
    next(error);
  }
});

app.post("/api/override", async (req, res, next) => {
  try {
    const { transaction_id, status, mindshare_category, note } = req.body;
    if (!transaction_id || !["included", "excluded", "review"].includes(status)) {
      res.status(400).json({ error: "transaction_id and valid status are required" });
      return;
    }

    const overrides = await readOverrides();
    overrides.set(transaction_id, {
      transaction_id,
      status,
      mindshare_category: mindshare_category || (status === "included" ? "manual-mindshare" : "manual"),
      note: note || ""
    });
    await writeOverrides(overrides);
    const { summary } = await classifyAll();
    res.json({ ok: true, summary });
  } catch (error) {
    next(error);
  }
});

app.post("/api/override-merchant", async (req, res, next) => {
  try {
    const { merchant, status, mindshare_category, note } = req.body;
    if (!merchant || !["included", "excluded", "review"].includes(status)) {
      res.status(400).json({ error: "merchant and valid status are required" });
      return;
    }

    const transactions = await readJson(txPath, []);
    const targetGroup = merchantGroup(merchant);
    const matches = transactions.filter((tx) => merchantGroup(tx.merchant_name || tx.name || "Unknown") === targetGroup);
    const overrides = await readOverrides();

    for (const tx of matches) {
      overrides.set(tx.transaction_id, {
        transaction_id: tx.transaction_id,
        status,
        mindshare_category: mindshare_category || (status === "included" ? "manual-mindshare" : "manual"),
        note: note || `merchant override: ${merchant}`
      });
    }

    await writeOverrides(overrides);
    const { summary } = await classifyAll();
    res.json({ ok: true, merchant: targetGroup, updated: matches.length, summary });
  } catch (error) {
    next(error);
  }
});

app.use((error, _req, res, _next) => {
  const plaidError = error?.response?.data;
  if (plaidError) {
    res.status(500).json(plaidError);
    return;
  }

  res.status(500).json({ error: error.message || "Unknown error" });
});

app.listen(port, () => {
  console.log(`Plaid trial app listening on http://localhost:${port}`);
});

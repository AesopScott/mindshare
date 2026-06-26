import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { classifyTransaction, parseCsvLine, summarizeClassifications, toCsv } from "./lib/classifier.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const dataDir = path.join(__dirname, "data");
const transactionsPath = path.join(dataDir, "transactions.json");
const outDir = path.join(__dirname, "reports");
const overridesPath = path.join(__dirname, "overrides.csv");

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

const transactions = JSON.parse(await fs.readFile(transactionsPath, "utf8"));
const overrides = await readOverrides();
const rows = transactions
  .map((tx) => classifyTransaction(tx, overrides))
  .sort((a, b) => b.date.localeCompare(a.date) || a.merchant.localeCompare(b.merchant));
const reviewRows = rows.filter((row) => row.status === "review");
const includedRows = rows.filter((row) => row.status === "included");
const summary = summarizeClassifications(rows);

await fs.mkdir(outDir, { recursive: true });
await fs.writeFile(path.join(outDir, "classified-transactions.csv"), `${toCsv(rows)}\n`);
await fs.writeFile(path.join(outDir, "mindshare-included.csv"), `${toCsv(includedRows)}\n`);
await fs.writeFile(path.join(outDir, "manual-review.csv"), `${toCsv(reviewRows)}\n`);
await fs.writeFile(path.join(outDir, "summary.json"), `${JSON.stringify(summary, null, 2)}\n`);

try {
  await fs.access(overridesPath);
} catch {
  await fs.writeFile(
    overridesPath,
    [
      "transaction_id,status,mindshare_category,note",
      "# status allowed: included,excluded,review",
      "# Use transaction_id from reports/manual-review.csv or reports/classified-transactions.csv"
    ].join("\n") + "\n"
  );
}

console.log(JSON.stringify(summary, null, 2));

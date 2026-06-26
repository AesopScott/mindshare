export const includePatterns = [
  ["ai-models", /openai|chatgpt|anthropic|claude|perplexity|mistral|groq|cohere|replicate|together|fireworks|hugging\s*face|elevenlabs|midjourney|runway/i],
  ["developer-tools", /github|copilot|cursor|windsurf|replit|vercel|netlify|render|railway|fly\.io|digitalocean|heroku|linear|atlassian|jira|slack/i],
  ["cloud-infra", /cloudflare|google cloud|gcp|amazon web services|aws|microsoft azure|azure|supabase|pinecone|qdrant|mongodb|neon|planetscale/i],
  ["software", /adobe|figma|notion|dropbox|google one|google workspace|microsoft|office|zoom|loom|canva|zapier|make\.com/i],
  ["internet-telecom", /comcast|xfinity|centurylink|quantum fiber|verizon|at&t|tmobile|t-mobile|spectrum|starlink/i],
  ["hardware", /apple|best buy|micro center|newegg|b&h|bh photo|lenovo|dell|hp\.com|anker/i],
  ["internet-domains", /godaddy|domainagents|domain\.com|namecheap|squarespace|wix|mochahost|bluehost|siteground/i],
  ["payments-platform", /paypal|stripe|wise/i]
];

const defaultIncludeCategoryPatterns = [
  /GENERAL_SERVICES_TELECOMMUNICATIONS/i,
  /GENERAL_MERCHANDISE_ELECTRONICS/i
];

const obviousPersonalCategoryPatterns = [
  /FOOD_AND_DRINK/i,
  /TRAVEL/i,
  /TRANSPORTATION/i,
  /ENTERTAINMENT/i,
  /MEDICAL/i,
  /RENT_AND_UTILITIES_GAS_AND_ELECTRICITY/i,
  /HOME_IMPROVEMENT/i,
  /GENERAL_MERCHANDISE_BOOKSTORES_AND_NEWSSTANDS/i,
  /PERSONAL_CARE/i,
  /GOVERNMENT_AND_NON_PROFIT/i
];

const reviewCategoryPatterns = [
  /GENERAL_MERCHANDISE/i,
  /GENERAL_SERVICES/i,
  /TRANSFER/i,
  /LOAN_PAYMENTS/i
];

const automaticExcludePatterns = [
  ["keep-the-change-transfer", /KEEP THE CHANGE TRANSFER/i]
];

export function csvEscape(value) {
  const stringValue = String(value ?? "");
  if (/[",\n\r]/.test(stringValue)) {
    return `"${stringValue.replaceAll('"', '""')}"`;
  }
  return stringValue;
}

export function parseCsvLine(line) {
  const result = [];
  let current = "";
  let quoted = false;

  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    const next = line[index + 1];
    if (char === '"' && quoted && next === '"') {
      current += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      result.push(current);
      current = "";
    } else {
      current += char;
    }
  }

  result.push(current);
  return result;
}

function textFor(tx) {
  return [
    tx.name,
    tx.merchant_name,
    tx.website,
    tx.personal_finance_category?.primary,
    tx.personal_finance_category?.detailed,
    tx.payment_channel,
    tx.mindshare_source_institution
  ]
    .filter(Boolean)
    .join(" ");
}

function merchant(tx) {
  return tx.merchant_name || tx.name || "Unknown";
}

export function merchantGroup(value) {
  const raw = String(value || "Unknown").trim();
  if (/KEEP THE CHANGE TRANSFER/i.test(raw)) return "KEEP THE CHANGE TRANSFER";
  if (/Online Banking transfer to/i.test(raw)) return "Online Banking transfer";
  if (/Online Banking payment to/i.test(raw)) return "Online Banking payment";
  if (/Bill Payment/i.test(raw)) return raw.replace(/\s+Bill Payment.*/i, " Bill Payment").trim();

  const desMatch = raw.match(/^(.+?)\s+DES:/i);
  if (desMatch) return cleanGroupName(desMatch[1]);

  const achMatch = raw.match(/^(.+?)\s+(ACH|PPD|CCD|WEB|TEL|ID:|INDN:|CO ID:|PMT INFO:)/i);
  if (achMatch) return cleanGroupName(achMatch[1]);

  return cleanGroupName(raw);
}

function cleanGroupName(value) {
  return String(value || "Unknown")
    .replace(/\b(?:ID|INDN|CO ID|WEB PMT INFO|PMT INFO|CONFIRMATION#|CONF#)\b.*$/i, "")
    .replace(/\b(?:XXXXX|AXXXXX|XXXXXXXXXX)[A-Z0-9-]*\b/gi, "")
    .replace(/\b[A-Z]?\d{4,}[A-Z0-9-]*\b/g, "")
    .replace(/\b\d{1,2}\/\d{1,2}\/\d{2,4}\b/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

export function classifyTransaction(tx, overrides = new Map()) {
  const haystack = textFor(tx);
  const reasons = [];
  let category = "not-mindshare";
  let status = "excluded";
  let confidence = "medium";

  for (const [label, pattern] of automaticExcludePatterns) {
    if (pattern.test(haystack)) {
      reasons.push(`automatic exclude ${label}`);
      const row = {
        transaction_id: tx.transaction_id,
        date: tx.date,
        source: tx.mindshare_source_institution,
        account_owner: tx.account_owner || "",
        merchant: merchant(tx),
        merchant_group: merchantGroup(merchant(tx)),
        name: tx.name || "",
        amount: Number(tx.amount || 0),
        pending: Boolean(tx.pending),
        plaid_primary: tx.personal_finance_category?.primary || "",
        plaid_detailed: tx.personal_finance_category?.detailed || "",
        status: "excluded",
        mindshare_category: "automatic-personal-transfer",
        confidence: "high",
        reason: reasons.join("; ")
      };

      const override = overrides.get(tx.transaction_id);
      if (override) {
        row.status = override.status || row.status;
        row.mindshare_category = override.mindshare_category || row.mindshare_category;
        row.confidence = "manual";
        row.reason = `manual override: ${override.note || "no note"}`;
      }

      return row;
    }
  }

  for (const [label, pattern] of includePatterns) {
    if (pattern.test(haystack)) {
      reasons.push(`matched ${label}`);
      category = label;
      status = "included";
      confidence = "high";
      break;
    }
  }

  if (status !== "included") {
    const detailed = tx.personal_finance_category?.detailed || "";
    const defaultCategoryHit = defaultIncludeCategoryPatterns.some((pattern) => pattern.test(detailed));
    if (defaultCategoryHit) {
      reasons.push(`default-in Plaid category ${detailed}`);
      category = "computer-internet-review";
      status = "included";
      confidence = "low";
    }
  }

  if (status !== "included") {
    const detailed = tx.personal_finance_category?.detailed || "";
    const primary = tx.personal_finance_category?.primary || "";
    const catText = `${primary} ${detailed}`;
    if (obviousPersonalCategoryPatterns.some((pattern) => pattern.test(catText))) {
      reasons.push(`obvious personal category ${detailed || primary}`);
      status = "excluded";
      confidence = "high";
    } else if (reviewCategoryPatterns.some((pattern) => pattern.test(catText))) {
      reasons.push(`needs owner review category ${detailed || primary}`);
      status = "review";
      confidence = "low";
      category = "manual-review";
    } else {
      reasons.push("no tech/internet signal");
      status = "review";
      confidence = "low";
      category = "manual-review";
    }
  }

  const row = {
    transaction_id: tx.transaction_id,
    date: tx.date,
    source: tx.mindshare_source_institution,
    account_owner: tx.account_owner || "",
    merchant: merchant(tx),
    merchant_group: merchantGroup(merchant(tx)),
    name: tx.name || "",
    amount: Number(tx.amount || 0),
    pending: Boolean(tx.pending),
    plaid_primary: tx.personal_finance_category?.primary || "",
    plaid_detailed: tx.personal_finance_category?.detailed || "",
    status,
    mindshare_category: category,
    confidence,
    reason: reasons.join("; ")
  };

  const override = overrides.get(tx.transaction_id);
  if (override) {
    row.status = override.status || row.status;
    row.mindshare_category = override.mindshare_category || row.mindshare_category;
    row.confidence = "manual";
    row.reason = `manual override: ${override.note || "no note"}`;
  }

  return row;
}

export function toCsv(rows) {
  const headers = [
    "transaction_id",
    "date",
    "source",
    "account_owner",
    "merchant",
    "name",
    "amount",
    "pending",
    "plaid_primary",
    "plaid_detailed",
    "status",
    "mindshare_category",
    "confidence",
    "reason"
  ];
  return [
    headers.join(","),
    ...rows.map((row) => headers.map((header) => csvEscape(row[header])).join(","))
  ].join("\n");
}

function monthKey(date) {
  return String(date).slice(0, 7);
}

function sortEntries(map) {
  return [...map.entries()]
    .map(([name, amount]) => ({ name, amount: Number(amount.toFixed(2)) }))
    .sort((a, b) => Math.abs(b.amount) - Math.abs(a.amount));
}

export function summarizeClassifications(rows) {
  const included = rows.filter((row) => row.status === "included");
  const review = rows.filter((row) => row.status === "review");
  const excluded = rows.filter((row) => row.status === "excluded");

  const byMonth = new Map();
  const byMerchant = new Map();
  const byCategory = new Map();

  for (const row of included) {
    byMonth.set(monthKey(row.date), (byMonth.get(monthKey(row.date)) || 0) + row.amount);
    byMerchant.set(row.merchant, (byMerchant.get(row.merchant) || 0) + row.amount);
    byCategory.set(row.mindshare_category, (byCategory.get(row.mindshare_category) || 0) + row.amount);
  }

  return {
    generated_at: new Date().toISOString(),
    transaction_count: rows.length,
    included_count: included.length,
    review_count: review.length,
    excluded_count: excluded.length,
    included_total: Number(included.reduce((sum, row) => sum + row.amount, 0).toFixed(2)),
    review_total: Number(review.reduce((sum, row) => sum + row.amount, 0).toFixed(2)),
    date_min: rows.map((row) => row.date).sort()[0],
    date_max: rows.map((row) => row.date).sort().at(-1),
    included_by_month: sortEntries(byMonth).sort((a, b) => a.name.localeCompare(b.name)),
    included_by_category: sortEntries(byCategory),
    included_by_merchant_top_40: sortEntries(byMerchant).slice(0, 40)
  };
}

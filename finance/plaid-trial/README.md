# Mindshare Plaid Trial

Local-only trial tool for Scott's Plaid Trial plan.

## Scope

- Uses Plaid `transactions` only.
- Stores linked Item access tokens in ignored local file `data/items.json`.
- Stores synced transactions in ignored local file `data/transactions.json`.
- Does not move money, approve spend, contact vendors, or write to external systems.

## Setup

1. Copy `.env.example` to `.env.local`.
2. Fill `PLAID_CLIENT_ID`, `PLAID_SECRET`, and `PLAID_ENV=production` from Plaid Dashboard Trial plan.
3. Run:

```powershell
npm install
npm start
```

4. Open `http://localhost:3333`.
5. Click `Link Account`.
6. Link one institution first.
7. Click `Sync Transactions`.

## Sensitive Data

`data/items.json` contains Plaid access tokens. Treat it like a secret.

Before deleting the local project or stopping Plaid use, remove Items through Plaid `/item/remove` or Plaid Dashboard/support so subscription products cannot remain active after upgrade.


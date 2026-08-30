-- ============================================================
-- Agentic Commerce Platform — SQLite Schema
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    upi_id          TEXT NOT NULL,
    bank_account    TEXT NOT NULL,
    spend_limit     REAL NOT NULL DEFAULT 0,
    passkey_verified INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS agents (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    agent_type  TEXT NOT NULL CHECK(agent_type IN ('buyer','merchant','dispute')),
    status      TEXT NOT NULL DEFAULT 'idle',
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS merchants (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    rating      REAL NOT NULL DEFAULT 4.5,
    location    TEXT NOT NULL,
    base_price  REAL NOT NULL,
    syndicate_partner_of TEXT
);

CREATE TABLE IF NOT EXISTS intents (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    raw_text     TEXT NOT NULL,
    item         TEXT,
    quantity     INTEGER,
    max_budget   REAL,
    parsed_json  TEXT,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS bids (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id   INTEGER NOT NULL REFERENCES intents(id),
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    quoted_price REAL NOT NULL,
    delivery_days REAL NOT NULL,
    offer_json  TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS deals (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id       INTEGER NOT NULL REFERENCES intents(id),
    merchant_id     INTEGER NOT NULL REFERENCES merchants(id),
    original_price  REAL NOT NULL,
    final_price     REAL NOT NULL,
    concessions     TEXT,
    deal_memo_json  TEXT NOT NULL,
    signature       TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS orders (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    deal_id             INTEGER NOT NULL REFERENCES deals(id),
    razorpay_order_id   TEXT NOT NULL,
    spt_token           TEXT,
    amount              REAL NOT NULL,
    status              TEXT NOT NULL DEFAULT 'created',
    created_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS splits (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        INTEGER NOT NULL REFERENCES orders(id),
    merchant_id     INTEGER NOT NULL REFERENCES merchants(id),
    amount          REAL NOT NULL,
    role            TEXT NOT NULL DEFAULT 'primary',
    payout_status   TEXT NOT NULL DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS escrow (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    INTEGER NOT NULL REFERENCES orders(id),
    amount      REAL NOT NULL,
    status      TEXT NOT NULL DEFAULT 'held',
    held_at     TEXT NOT NULL DEFAULT (datetime('now')),
    released_at TEXT
);

CREATE TABLE IF NOT EXISTS poi_bundles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    INTEGER NOT NULL REFERENCES orders(id),
    bundle_json TEXT NOT NULL,
    signature   TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS disputes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        INTEGER NOT NULL REFERENCES orders(id),
    reason          TEXT NOT NULL,
    delivered_desc  TEXT,
    status          TEXT NOT NULL DEFAULT 'open',
    resolution      TEXT,
    refund_amount   REAL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    resolved_at     TEXT
);
-- Adds the General Ledger core: account_types, accounts, sub_accounts,
-- account_sub_accounts, fiscal_periods, journal_vouchers,
-- subaccount_entries. Bank Deposits/Reconciliation are a separate,
-- not-yet-built module.

BEGIN;

CREATE TABLE IF NOT EXISTS account_types (
    account_type_id  SERIAL PRIMARY KEY,
    name              TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id       SERIAL PRIMARY KEY,
    account_no        TEXT NOT NULL UNIQUE,
    name               TEXT NOT NULL,
    account_type_id     INTEGER NOT NULL REFERENCES account_types(account_type_id)
);

CREATE TABLE IF NOT EXISTS sub_accounts (
    sub_account_id   SERIAL PRIMARY KEY,
    name              TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS account_sub_accounts (
    acc_sub_acc_id   SERIAL PRIMARY KEY,
    account_id        INTEGER NOT NULL REFERENCES accounts(account_id),
    sub_account_id      INTEGER NOT NULL REFERENCES sub_accounts(sub_account_id),
    UNIQUE (account_id, sub_account_id)
);

CREATE TABLE IF NOT EXISTS fiscal_periods (
    fiscal_period_id  SERIAL PRIMARY KEY,
    name               TEXT NOT NULL,
    start_date          DATE NOT NULL,
    end_date             DATE NOT NULL,
    is_closed             BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS journal_vouchers (
    journal_voucher_id  SERIAL PRIMARY KEY,
    description           TEXT NOT NULL,
    transaction_datetime    TIMESTAMPTZ NOT NULL DEFAULT now(),
    source_reference          TEXT,
    fiscal_period_id           INTEGER REFERENCES fiscal_periods(fiscal_period_id),
    created_by                   INTEGER REFERENCES system_users(system_user_id)
);

CREATE TABLE IF NOT EXISTS subaccount_entries (
    subaccount_entry_id  SERIAL PRIMARY KEY,
    journal_voucher_id     INTEGER NOT NULL REFERENCES journal_vouchers(journal_voucher_id) ON DELETE CASCADE,
    acc_sub_acc_id           INTEGER NOT NULL REFERENCES account_sub_accounts(acc_sub_acc_id),
    entry_type                 TEXT NOT NULL CHECK (entry_type IN ('Debit', 'Credit')),
    amount                       NUMERIC(14,2) NOT NULL CHECK (amount > 0),
    transaction_datetime           TIMESTAMPTZ NOT NULL DEFAULT now(),
    fiscal_period_id                 INTEGER REFERENCES fiscal_periods(fiscal_period_id)
);

CREATE INDEX IF NOT EXISTS idx_subaccount_entries_journal_voucher_id ON subaccount_entries (journal_voucher_id);
CREATE INDEX IF NOT EXISTS idx_subaccount_entries_acc_sub_acc_id ON subaccount_entries (acc_sub_acc_id);

INSERT INTO account_types (name) VALUES ('Asset'), ('Liability'), ('Equity'), ('Income'), ('Expense')
ON CONFLICT (name) DO NOTHING;

COMMIT;

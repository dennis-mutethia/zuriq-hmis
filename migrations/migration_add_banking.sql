-- Adds Banking: banks, bank_branches, bank_deposits,
-- bank_reconciliations, bank_rec_items. Requires the GL core
-- (migration_add_general_ledger.sql) to already be applied.

BEGIN;

CREATE TABLE IF NOT EXISTS banks (
    bank_id     SERIAL PRIMARY KEY,
    name         TEXT NOT NULL,
    bank_code      TEXT
);

CREATE TABLE IF NOT EXISTS bank_branches (
    bank_branch_id  SERIAL PRIMARY KEY,
    bank_id           INTEGER NOT NULL REFERENCES banks(bank_id),
    name                TEXT NOT NULL,
    branch_code           TEXT
);

CREATE TABLE IF NOT EXISTS bank_deposits (
    bank_deposit_id       SERIAL PRIMARY KEY,
    dest_acc_sub_acc_id     INTEGER NOT NULL REFERENCES account_sub_accounts(acc_sub_acc_id),
    source_acc_sub_acc_id     INTEGER REFERENCES account_sub_accounts(acc_sub_acc_id),
    journal_voucher_id           INTEGER REFERENCES journal_vouchers(journal_voucher_id),
    amount                          NUMERIC(14,2) NOT NULL CHECK (amount > 0),
    bank_transaction_ref_no           TEXT,
    cheque_nos                          TEXT,
    deposited_by                          INTEGER REFERENCES system_users(system_user_id),
    date_time_deposited                     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS bank_reconciliations (
    bank_rec_id       SERIAL PRIMARY KEY,
    acc_sub_acc_id      INTEGER NOT NULL REFERENCES account_sub_accounts(acc_sub_acc_id),
    from_date              DATE NOT NULL,
    to_date                  DATE NOT NULL,
    book_balance               NUMERIC(14,2) NOT NULL,
    statement_balance            NUMERIC(14,2) NOT NULL,
    has_been_reconciled            BOOLEAN NOT NULL DEFAULT FALSE,
    reconciled_by                    INTEGER REFERENCES system_users(system_user_id),
    reconciled_at                      TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS bank_rec_items (
    bank_rec_item_id  SERIAL PRIMARY KEY,
    bank_rec_id         INTEGER NOT NULL REFERENCES bank_reconciliations(bank_rec_id) ON DELETE CASCADE,
    subaccount_entry_id   INTEGER REFERENCES subaccount_entries(subaccount_entry_id),
    description             TEXT NOT NULL,
    amount                    NUMERIC(14,2) NOT NULL,
    side                        TEXT NOT NULL CHECK (side IN ('bank', 'book')),
    is_increment                  BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_bank_branches_bank_id ON bank_branches (bank_id);
CREATE INDEX IF NOT EXISTS idx_bank_deposits_dest_acc_sub_acc_id ON bank_deposits (dest_acc_sub_acc_id);
CREATE INDEX IF NOT EXISTS idx_bank_reconciliations_acc_sub_acc_id ON bank_reconciliations (acc_sub_acc_id);
CREATE INDEX IF NOT EXISTS idx_bank_rec_items_bank_rec_id ON bank_rec_items (bank_rec_id);

COMMIT;

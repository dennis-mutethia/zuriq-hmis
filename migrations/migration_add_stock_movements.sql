-- Adds a stock movement ledger (every intake and dispense event against a
-- product) to an existing database. Products/prescriptions must already
-- exist (migration_add_pharmacy.sql).

BEGIN;

CREATE TABLE IF NOT EXISTS stock_movements (
    stock_movement_id  SERIAL PRIMARY KEY,
    product_id           INTEGER NOT NULL REFERENCES products(product_id),
    quantity_change       INTEGER NOT NULL,
    reason                 TEXT NOT NULL,
    recorded_by            INTEGER REFERENCES system_users(system_user_id),
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_stock_movements_product_id ON stock_movements (product_id);

COMMIT;

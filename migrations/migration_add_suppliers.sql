-- Adds suppliers and links them to stock intake movements. Requires
-- stock_movements to already exist (migration_add_stock_movements.sql).

BEGIN;

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id      SERIAL PRIMARY KEY,
    name              TEXT NOT NULL,
    contact_person    TEXT,
    telephone         TEXT,
    email             TEXT,
    is_active         BOOLEAN NOT NULL DEFAULT TRUE
);

ALTER TABLE stock_movements ADD COLUMN IF NOT EXISTS supplier_id INTEGER REFERENCES suppliers(supplier_id);

CREATE INDEX IF NOT EXISTS idx_stock_movements_supplier_id ON stock_movements (supplier_id);

COMMIT;

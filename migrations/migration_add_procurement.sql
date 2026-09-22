-- Adds Procurement: purchase_orders, purchase_order_items, grns,
-- grn_items. Requires suppliers and products to already exist
-- (migration_add_suppliers.sql, migration_add_pharmacy.sql).

BEGIN;

CREATE TABLE IF NOT EXISTS purchase_orders (
    purchase_order_id     SERIAL PRIMARY KEY,
    purchase_order_no       TEXT UNIQUE,
    supplier_id               INTEGER NOT NULL REFERENCES suppliers(supplier_id),
    order_reference             TEXT,
    prepared_by                   INTEGER REFERENCES system_users(system_user_id),
    checked_by                      INTEGER REFERENCES system_users(system_user_id),
    date_time_issued                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    date_time_checked                   TIMESTAMPTZ,
    has_been_checked                      BOOLEAN NOT NULL DEFAULT FALSE,
    has_been_received                       BOOLEAN NOT NULL DEFAULT FALSE,
    delivery_note_no                          TEXT,
    invoice_no                                  TEXT,
    terms_conditions                              TEXT,
    validity_date                                   DATE
);

CREATE TABLE IF NOT EXISTS purchase_order_items (
    purchase_order_item_id  SERIAL PRIMARY KEY,
    purchase_order_id         INTEGER NOT NULL REFERENCES purchase_orders(purchase_order_id) ON DELETE CASCADE,
    product_id                   INTEGER REFERENCES products(product_id),
    name                             TEXT NOT NULL,
    quantity                             INTEGER NOT NULL DEFAULT 1,
    rate                                     NUMERIC(14,2) NOT NULL DEFAULT 0,
    amount                                     NUMERIC(14,2) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS grns (
    grn_id                 SERIAL PRIMARY KEY,
    grn_no                   TEXT UNIQUE,
    purchase_order_id          INTEGER NOT NULL REFERENCES purchase_orders(purchase_order_id),
    delivery_note_no              TEXT,
    ap_invoice_no                   TEXT,
    date_time_created                 TIMESTAMPTZ NOT NULL DEFAULT now(),
    has_been_checked                    BOOLEAN NOT NULL DEFAULT FALSE,
    is_committed_to_stock                 BOOLEAN NOT NULL DEFAULT FALSE,
    created_by                              INTEGER REFERENCES system_users(system_user_id)
);

CREATE TABLE IF NOT EXISTS grn_items (
    grn_item_id           SERIAL PRIMARY KEY,
    grn_id                  INTEGER NOT NULL REFERENCES grns(grn_id) ON DELETE CASCADE,
    purchase_order_item_id     INTEGER REFERENCES purchase_order_items(purchase_order_item_id),
    product_id                     INTEGER NOT NULL REFERENCES products(product_id),
    quantity_ordered                  INTEGER,
    quantity_received                   INTEGER NOT NULL DEFAULT 0,
    rate                                   NUMERIC(14,2) NOT NULL DEFAULT 0,
    batch_no                                 TEXT,
    earliest_expiry_date                       DATE
);

CREATE INDEX IF NOT EXISTS idx_purchase_order_items_po_id ON purchase_order_items (purchase_order_id);
CREATE INDEX IF NOT EXISTS idx_grns_purchase_order_id ON grns (purchase_order_id);
CREATE INDEX IF NOT EXISTS idx_grn_items_grn_id ON grn_items (grn_id);

CREATE OR REPLACE FUNCTION assign_po_number()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE purchase_orders
    SET purchase_order_no = COALESCE(purchase_order_no, 'ZH-PO-' || NEW.purchase_order_id)
    WHERE purchase_order_id = NEW.purchase_order_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_assign_po_number ON purchase_orders;
CREATE TRIGGER trg_assign_po_number
AFTER INSERT ON purchase_orders
FOR EACH ROW
EXECUTE FUNCTION assign_po_number();

CREATE OR REPLACE FUNCTION assign_grn_number()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE grns
    SET grn_no = COALESCE(grn_no, 'ZH-GRN-' || NEW.grn_id)
    WHERE grn_id = NEW.grn_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_assign_grn_number ON grns;
CREATE TRIGGER trg_assign_grn_number
AFTER INSERT ON grns
FOR EACH ROW
EXECUTE FUNCTION assign_grn_number();

COMMIT;

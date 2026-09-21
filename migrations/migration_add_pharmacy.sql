-- Adds the Pharmacy/Dispensing module (products, prescriptions,
-- prescription_items) to an existing database.

BEGIN;

CREATE TABLE IF NOT EXISTS products (
    product_id         SERIAL PRIMARY KEY,
    code               TEXT,
    name               TEXT NOT NULL,
    description        TEXT,
    unit_definition    TEXT,
    unit_cost          NUMERIC(14,2) NOT NULL DEFAULT 0,
    unit_price         NUMERIC(14,2) NOT NULL DEFAULT 0,
    quantity_in_stock  INTEGER NOT NULL DEFAULT 0,
    reorder_level      INTEGER NOT NULL DEFAULT 0,
    is_active          BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id    SERIAL PRIMARY KEY,
    visit_id            INTEGER REFERENCES visits(visit_id),
    patient_id          INTEGER NOT NULL REFERENCES patients(patient_id),
    prescribed_by       TEXT,
    special_instruction TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS prescription_items (
    prescription_item_id  SERIAL PRIMARY KEY,
    prescription_id        INTEGER NOT NULL REFERENCES prescriptions(prescription_id) ON DELETE CASCADE,
    product_id              INTEGER REFERENCES products(product_id),
    inscription              TEXT NOT NULL,
    quantity                  INTEGER NOT NULL DEFAULT 1,
    quantity_per_time        TEXT,
    frequency_per_day        TEXT,
    dosage_duration          TEXT,
    other_instruction        TEXT,
    has_been_dispensed       BOOLEAN NOT NULL DEFAULT FALSE,
    dispensed_at             TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_prescriptions_visit_id ON prescriptions (visit_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_patient_id ON prescriptions (patient_id);
CREATE INDEX IF NOT EXISTS idx_prescription_items_prescription_id ON prescription_items (prescription_id);

COMMIT;

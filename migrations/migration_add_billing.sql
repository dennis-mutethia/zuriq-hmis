-- Adds the Billing module (services, medical_bills, bill_items) to an
-- existing database that already has patients + visits set up.

BEGIN;

CREATE TABLE IF NOT EXISTS services (
    service_id         SERIAL PRIMARY KEY,
    name               TEXT NOT NULL,
    department_id      INTEGER,
    cash_rate          NUMERIC(14,2) NOT NULL DEFAULT 0,
    nhif_rate          NUMERIC(14,2),
    aar_rate           NUMERIC(14,2),
    kcb_rate           NUMERIC(14,2),
    eduafya_rate       NUMERIC(14,2),
    liason_rate        NUMERIC(14,2),
    national_scheme_rate NUMERIC(14,2),
    is_active          BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS medical_bills (
    medical_bill_id       SERIAL PRIMARY KEY,
    medical_bill_no       TEXT UNIQUE,
    visit_id              INTEGER REFERENCES visits(visit_id),
    patient_id            INTEGER REFERENCES patients(patient_id),
    is_patient            BOOLEAN NOT NULL DEFAULT TRUE,
    customer_name         TEXT,
    telephone_no          TEXT,
    id_number             TEXT,
    group_account_id      INTEGER REFERENCES group_accounts(group_account_id),
    total_bill_amount     NUMERIC(14,2) NOT NULL DEFAULT 0,
    sales_discount_amount NUMERIC(14,2) NOT NULL DEFAULT 0,
    write_off_amount      NUMERIC(14,2) NOT NULL DEFAULT 0,
    cover_amount          NUMERIC(14,2) NOT NULL DEFAULT 0,
    advance_payment       NUMERIC(14,2) NOT NULL DEFAULT 0,
    total_amount_paid     NUMERIC(14,2) NOT NULL DEFAULT 0,
    deposit_balance       NUMERIC(14,2) NOT NULL DEFAULT 0,
    deposit_offset        NUMERIC(14,2) NOT NULL DEFAULT 0,
    is_processed          BOOLEAN NOT NULL DEFAULT FALSE,
    date_time_created     TIMESTAMPTZ NOT NULL DEFAULT now(),
    date_time_processed   TIMESTAMPTZ,
    processed_by          INTEGER REFERENCES system_users(system_user_id)
);

CREATE TABLE IF NOT EXISTS bill_items (
    bill_item_id        SERIAL PRIMARY KEY,
    medical_bill_id      INTEGER NOT NULL REFERENCES medical_bills(medical_bill_id) ON DELETE CASCADE,
    service_id           INTEGER REFERENCES services(service_id),
    name                 TEXT NOT NULL,
    quantity              INTEGER NOT NULL DEFAULT 1,
    rate                  NUMERIC(14,2) NOT NULL DEFAULT 0,
    percentage_discount   NUMERIC(5,2) NOT NULL DEFAULT 0,
    discounted_amount     NUMERIC(14,2) NOT NULL DEFAULT 0,
    amount                NUMERIC(14,2) NOT NULL DEFAULT 0,
    has_been_paid_for     BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_medical_bills_visit_id ON medical_bills (visit_id);
CREATE INDEX IF NOT EXISTS idx_medical_bills_patient_id ON medical_bills (patient_id);
CREATE INDEX IF NOT EXISTS idx_bill_items_medical_bill_id ON bill_items (medical_bill_id);

CREATE OR REPLACE FUNCTION assign_medical_bill_number()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE medical_bills
    SET medical_bill_no = COALESCE(medical_bill_no, 'ZH-MB-' || NEW.medical_bill_id)
    WHERE medical_bill_id = NEW.medical_bill_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_assign_medical_bill_number ON medical_bills;
CREATE TRIGGER trg_assign_medical_bill_number
AFTER INSERT ON medical_bills
FOR EACH ROW
EXECUTE FUNCTION assign_medical_bill_number();

COMMIT;

-- Run this INSTEAD of schema.sql if you already created the patients table
-- with out_patient_no/in_patient_no as INTEGER. Safe to run even with
-- existing patient rows — it converts the columns and backfills numbers
-- for any rows that don't already have the ZH- format.

BEGIN;

-- 1. Widen the columns to text
ALTER TABLE patients ALTER COLUMN out_patient_no TYPE TEXT USING out_patient_no::TEXT;
ALTER TABLE patients ALTER COLUMN in_patient_no  TYPE TEXT USING in_patient_no::TEXT;

-- 2. Add a uniqueness constraint on in_patient_no (out_patient_no already has one)
ALTER TABLE patients ADD CONSTRAINT patients_in_patient_no_unique UNIQUE (in_patient_no);

-- 3. Install the auto-generation trigger for OUTPATIENT numbers only.
--    in_patient_no is intentionally left alone — it should only be set when
--    a patient is actually admitted (Admission module, not built yet), not
--    for every patient at registration.
CREATE OR REPLACE FUNCTION assign_outpatient_number()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE patients
    SET out_patient_no = COALESCE(out_patient_no, 'ZH-OP-' || NEW.patient_id)
    WHERE patient_id = NEW.patient_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_assign_patient_numbers ON patients; -- old name, if present
DROP TRIGGER IF EXISTS trg_assign_outpatient_number ON patients;
CREATE TRIGGER trg_assign_outpatient_number
AFTER INSERT ON patients
FOR EACH ROW
EXECUTE FUNCTION assign_outpatient_number();

CREATE OR REPLACE FUNCTION assign_inpatient_number(p_patient_id INTEGER)
RETURNS TEXT AS $$
DECLARE
    v_ip_no TEXT;
BEGIN
    UPDATE patients
    SET in_patient_no = COALESCE(in_patient_no, 'ZH-IP-' || p_patient_id)
    WHERE patient_id = p_patient_id
    RETURNING in_patient_no INTO v_ip_no;
    RETURN v_ip_no;
END;
$$ LANGUAGE plpgsql;

-- 4. Backfill any existing OUTPATIENT rows that don't already have the new
--    format. NOTE: this does NOT touch in_patient_no — if you'd previously
--    populated it for every patient, leave existing values as-is (or null
--    them out yourself if they were placeholders) rather than backfilling
--    it here, since not every patient should have one.
UPDATE patients
SET out_patient_no = 'ZH-OP-' || patient_id
WHERE out_patient_no IS NULL OR out_patient_no !~ '^ZH-OP-';

COMMIT;

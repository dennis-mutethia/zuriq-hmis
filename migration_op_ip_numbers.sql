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

-- 3. Install the auto-generation trigger
CREATE OR REPLACE FUNCTION assign_patient_numbers()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE patients
    SET out_patient_no = COALESCE(out_patient_no, 'ZH-OP-' || NEW.patient_id),
        in_patient_no  = COALESCE(in_patient_no,  'ZH-IP-' || NEW.patient_id)
    WHERE patient_id = NEW.patient_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_assign_patient_numbers ON patients;
CREATE TRIGGER trg_assign_patient_numbers
AFTER INSERT ON patients
FOR EACH ROW
EXECUTE FUNCTION assign_patient_numbers();

-- 4. Backfill any existing rows that don't already have the new format
UPDATE patients
SET out_patient_no = 'ZH-OP-' || patient_id
WHERE out_patient_no IS NULL OR out_patient_no !~ '^ZH-OP-';

UPDATE patients
SET in_patient_no = 'ZH-IP-' || patient_id
WHERE in_patient_no IS NULL OR in_patient_no !~ '^ZH-IP-';

COMMIT;

-- Adds Admission Diagnosis and a real discharge workflow (outcome,
-- discharge diagnosis, notes, medication) to admissions, plus a 'theatre'
-- room function so patients can be queued to theatre the same way as any
-- other room.

BEGIN;

ALTER TABLE admissions ADD COLUMN IF NOT EXISTS admission_diagnosis TEXT;
ALTER TABLE admissions ADD COLUMN IF NOT EXISTS discharge_outcome TEXT;
ALTER TABLE admissions DROP CONSTRAINT IF EXISTS admissions_discharge_outcome_check;
ALTER TABLE admissions ADD CONSTRAINT admissions_discharge_outcome_check
    CHECK (discharge_outcome IN ('Alive', 'Deceased', 'Referred', 'Discharged Against Medical Advice'));
ALTER TABLE admissions ADD COLUMN IF NOT EXISTS discharge_diagnosis TEXT;
ALTER TABLE admissions ADD COLUMN IF NOT EXISTS discharge_notes TEXT;
ALTER TABLE admissions ADD COLUMN IF NOT EXISTS discharge_medication TEXT;
ALTER TABLE admissions ADD COLUMN IF NOT EXISTS discharged_by INTEGER REFERENCES system_users(system_user_id);

ALTER TABLE rooms DROP CONSTRAINT IF EXISTS rooms_function_check;
ALTER TABLE rooms ADD CONSTRAINT rooms_function_check
    CHECK (function IN ('triage', 'consultation', 'lab', 'pharmacy', 'billing', 'reception', 'theatre'));

COMMIT;

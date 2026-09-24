-- Adds Chief Complaint, Past Medical History, and Examination to visits
-- — part of building out the Doctor Consultation screen into a real
-- clinical note (HPI/Diagnosis already existed).

BEGIN;

ALTER TABLE visits ADD COLUMN IF NOT EXISTS chief_complaint TEXT;
ALTER TABLE visits ADD COLUMN IF NOT EXISTS past_medical_history TEXT;
ALTER TABLE visits ADD COLUMN IF NOT EXISTS examination TEXT;

COMMIT;

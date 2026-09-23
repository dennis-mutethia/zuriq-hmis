-- Adds a diagnosis field to visits, part of the new Doctor Consultation
-- step (previously only doctor/hpi/summary existed, and only ever set
-- once at registration — no dedicated post-triage consultation step).

BEGIN;

ALTER TABLE visits ADD COLUMN IF NOT EXISTS diagnosis TEXT;

COMMIT;

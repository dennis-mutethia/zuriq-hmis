-- Adds the OPD Visits module (clinics + visits) to an existing database
-- that already has the patients table set up. Safe to run on its own.

BEGIN;

CREATE TABLE IF NOT EXISTS clinics (
    clinic_id   SERIAL PRIMARY KEY,
    name        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS visits (
    visit_id          SERIAL PRIMARY KEY,
    patient_id        INTEGER NOT NULL REFERENCES patients(patient_id),
    clinic_id         INTEGER REFERENCES clinics(clinic_id),
    visit_datetime    TIMESTAMPTZ NOT NULL DEFAULT now(),
    age               INTEGER,
    age_months        INTEGER,
    age_weeks         INTEGER,
    doctor            TEXT,
    nurse             TEXT,
    hpi               TEXT,
    summary           TEXT,
    is_processed      BOOLEAN NOT NULL DEFAULT FALSE,
    is_admitted       BOOLEAN NOT NULL DEFAULT FALSE,
    is_consultant     BOOLEAN NOT NULL DEFAULT FALSE,
    registered_by     INTEGER REFERENCES system_users(system_user_id)
);

CREATE INDEX IF NOT EXISTS idx_visits_patient_id ON visits (patient_id);
CREATE INDEX IF NOT EXISTS idx_visits_visit_datetime ON visits (visit_datetime);

COMMIT;

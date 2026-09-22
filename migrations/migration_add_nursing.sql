-- Adds the Nursing/Vitals module: nurse_triage (OPD, per visit) and
-- observation_charts (inpatient, repeated readings per admission).

BEGIN;

CREATE TABLE IF NOT EXISTS nurse_triage (
    nurse_triage_id          SERIAL PRIMARY KEY,
    visit_id                   INTEGER NOT NULL REFERENCES visits(visit_id),
    blood_pressure              TEXT,
    blood_pressure_remarks      TEXT,
    pulse_rate                   NUMERIC(5,1),
    pulse_rate_remarks           TEXT,
    respiration_rate             NUMERIC(5,1),
    respiration_rate_remarks     TEXT,
    temperature                   NUMERIC(4,1),
    temperature_remarks           TEXT,
    weight                         NUMERIC(6,2),
    weight_remarks                 TEXT,
    notes                           TEXT,
    recorded_by                     INTEGER REFERENCES system_users(system_user_id),
    created_at                       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_nurse_triage_visit_id ON nurse_triage (visit_id);

CREATE TABLE IF NOT EXISTS observation_charts (
    observation_id      SERIAL PRIMARY KEY,
    admission_id           INTEGER NOT NULL REFERENCES admissions(admission_id),
    systolic                 NUMERIC(5,1),
    diastolic                 NUMERIC(5,1),
    pulse                     NUMERIC(5,1),
    respiratory               NUMERIC(5,1),
    spo2                       NUMERIC(5,1),
    temperature                 NUMERIC(4,1),
    comments                     TEXT,
    recorded_by                   INTEGER REFERENCES system_users(system_user_id),
    created_at                     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_observation_charts_admission_id ON observation_charts (admission_id);

COMMIT;

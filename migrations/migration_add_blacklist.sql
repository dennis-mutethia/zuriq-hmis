-- Adds Patient Blacklist as an append-only history log (matching the
-- original's shape: each row is a blacklist or clear event, not a single
-- status flag) — a patient's current status is their most recent entry.

BEGIN;

CREATE TABLE IF NOT EXISTS patient_blacklist_entries (
    blacklist_entry_id  SERIAL PRIMARY KEY,
    patient_id             INTEGER NOT NULL REFERENCES patients(patient_id),
    is_blacklisted           BOOLEAN NOT NULL,
    reason                     TEXT,
    recorded_by                 INTEGER REFERENCES system_users(system_user_id),
    date_time_recorded             TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_patient_blacklist_entries_patient_id ON patient_blacklist_entries (patient_id, date_time_recorded DESC);

COMMIT;

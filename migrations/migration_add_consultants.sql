-- Adds Consultants: consultants, consultant_bookings, and links
-- visits.consultant_id to the real entity (previously just free text).

BEGIN;

CREATE TABLE IF NOT EXISTS consultants (
    consultant_id  SERIAL PRIMARY KEY,
    surname          TEXT NOT NULL,
    other_names        TEXT NOT NULL,
    alias                TEXT,
    designation            TEXT,
    mobile_no                TEXT,
    is_active                  BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS consultant_bookings (
    consultant_booking_id  SERIAL PRIMARY KEY,
    consultant_id            INTEGER NOT NULL REFERENCES consultants(consultant_id),
    patient_id                 INTEGER NOT NULL REFERENCES patients(patient_id),
    visit_datetime                TIMESTAMPTZ,
    datetime_booked                 TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_seen                            BOOLEAN NOT NULL DEFAULT FALSE,
    booked_by                            INTEGER REFERENCES system_users(system_user_id)
);

CREATE INDEX IF NOT EXISTS idx_consultant_bookings_consultant_id ON consultant_bookings (consultant_id);
CREATE INDEX IF NOT EXISTS idx_consultant_bookings_patient_id ON consultant_bookings (patient_id);

ALTER TABLE visits ADD COLUMN IF NOT EXISTS consultant_id INTEGER REFERENCES consultants(consultant_id);

COMMIT;

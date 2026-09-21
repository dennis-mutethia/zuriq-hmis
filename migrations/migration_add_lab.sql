-- Adds the Lab module (tests, lab_requests, lab_request_items) to an
-- existing database.

BEGIN;

CREATE TABLE IF NOT EXISTS tests (
    test_id     SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    specimen    TEXT,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS lab_requests (
    lab_request_id      SERIAL PRIMARY KEY,
    visit_id              INTEGER REFERENCES visits(visit_id),
    patient_id             INTEGER NOT NULL REFERENCES patients(patient_id),
    requested_by           INTEGER REFERENCES system_users(system_user_id),
    technologist            TEXT,
    date_time_requested     TIMESTAMPTZ NOT NULL DEFAULT now(),
    date_time_done          TIMESTAMPTZ,
    is_done                 BOOLEAN NOT NULL DEFAULT FALSE,
    reason_not_done         TEXT
);

CREATE TABLE IF NOT EXISTS lab_request_items (
    lab_request_item_id  SERIAL PRIMARY KEY,
    lab_request_id         INTEGER NOT NULL REFERENCES lab_requests(lab_request_id) ON DELETE CASCADE,
    test_id                 INTEGER REFERENCES tests(test_id),
    test_name               TEXT NOT NULL,
    conclusion               TEXT
);

CREATE INDEX IF NOT EXISTS idx_lab_requests_visit_id ON lab_requests (visit_id);
CREATE INDEX IF NOT EXISTS idx_lab_requests_patient_id ON lab_requests (patient_id);
CREATE INDEX IF NOT EXISTS idx_lab_request_items_lab_request_id ON lab_request_items (lab_request_id);

COMMIT;

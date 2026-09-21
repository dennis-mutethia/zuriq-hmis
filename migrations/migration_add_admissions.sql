-- Adds the Admissions module (wards, beds, admissions, admission_ward) to
-- an existing database. Requires assign_inpatient_number() to already
-- exist (added by migration_op_ip_numbers.sql / the current schema.sql).

BEGIN;

CREATE TABLE IF NOT EXISTS wards (
    ward_id     SERIAL PRIMARY KEY,
    name        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS beds (
    bed_id      SERIAL PRIMARY KEY,
    ward_id     INTEGER NOT NULL REFERENCES wards(ward_id),
    bed_no      TEXT NOT NULL,
    bed_status  TEXT NOT NULL DEFAULT 'Vacant' CHECK (bed_status IN ('Vacant', 'Occupied')),
    UNIQUE (ward_id, bed_no)
);

CREATE TABLE IF NOT EXISTS admissions (
    admission_id          SERIAL PRIMARY KEY,
    visit_id               INTEGER REFERENCES visits(visit_id),
    patient_id             INTEGER NOT NULL REFERENCES patients(patient_id),
    admission_datetime     TIMESTAMPTZ NOT NULL DEFAULT now(),
    discharge_datetime     TIMESTAMPTZ,
    is_in_admission        BOOLEAN NOT NULL DEFAULT TRUE,
    admitted_by            INTEGER REFERENCES system_users(system_user_id),
    admitting_doctor       TEXT,
    discharging_doctor     TEXT,
    received_by_nurse      TEXT
);

CREATE TABLE IF NOT EXISTS admission_ward (
    admission_ward_id  SERIAL PRIMARY KEY,
    admission_id        INTEGER NOT NULL REFERENCES admissions(admission_id),
    ward_id              INTEGER NOT NULL REFERENCES wards(ward_id),
    bed_id               INTEGER NOT NULL REFERENCES beds(bed_id),
    is_current_bed       BOOLEAN NOT NULL DEFAULT TRUE,
    assigned_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_admissions_patient_id ON admissions (patient_id);
CREATE INDEX IF NOT EXISTS idx_admissions_is_in_admission ON admissions (is_in_admission);
CREATE INDEX IF NOT EXISTS idx_admission_ward_admission_id ON admission_ward (admission_id);

CREATE OR REPLACE FUNCTION on_admission_created()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM assign_inpatient_number(NEW.patient_id);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_on_admission_created ON admissions;
CREATE TRIGGER trg_on_admission_created
AFTER INSERT ON admissions
FOR EACH ROW
EXECUTE FUNCTION on_admission_created();

COMMIT;

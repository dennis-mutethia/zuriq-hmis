-- Zuriq-HMIS → Supabase (PostgreSQL) schema
-- Module: Patient Registration
--
-- Source of truth: extracted from the decompiled Carepoint 3.2 source
-- (tblpatients, tblgroupaccounts, tblnationality, tblidtypes, tblsystemusers).
-- Column names below are modernized to snake_case; the original MySQL
-- column name is noted in a comment where it differs.
--
-- Run this in the Supabase SQL Editor (Project -> SQL Editor -> New query).
--
-- NOTE: if you already ran an earlier version of this file (with
-- out_patient_no/in_patient_no as INTEGER), don't re-run this — use
-- migration_op_ip_numbers.sql instead, which alters the existing table
-- in place without losing data.

-- ── Lookup tables ────────────────────────────────────────────────────────

CREATE TABLE id_types (
    id_type_id   SERIAL PRIMARY KEY,
    id_type      TEXT NOT NULL          -- original: IDType (e.g. 'National ID', 'Passport')
);

CREATE TABLE nationalities (
    nationality_id  SERIAL PRIMARY KEY,
    name            TEXT NOT NULL
);

CREATE TABLE group_accounts (
    group_account_id        SERIAL PRIMARY KEY,
    name                     TEXT NOT NULL,          -- corporate/insurance account name
    physical_address         TEXT,
    postal_address           TEXT,
    postal_code              TEXT,
    town_city                TEXT,
    telephone1               TEXT,
    email_address            TEXT,
    is_active                BOOLEAN NOT NULL DEFAULT TRUE,
    has_co_pay               BOOLEAN NOT NULL DEFAULT FALSE,
    co_pay_amount            NUMERIC(14,2) NOT NULL DEFAULT 0,
    contract_amount          NUMERIC(14,2) NOT NULL DEFAULT 0,
    credit_limit             NUMERIC(14,2) NOT NULL DEFAULT 0,
    has_visit_days_cap       BOOLEAN NOT NULL DEFAULT FALSE,
    capping_days             INTEGER,
    receivable_acc_sub_acc_id INTEGER  -- FK into accounting module (not built yet) — left unconstrained for now
);

-- Stub only: the real Security/Users module (auth, roles, permissions,
-- password hashing) is a separate module. This exists so patients.registered_by
-- has something to reference.
CREATE TABLE system_users (
    system_user_id  SERIAL PRIMARY KEY,
    username         TEXT NOT NULL UNIQUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Core table ───────────────────────────────────────────────────────────

CREATE TABLE patients (
    patient_id               SERIAL PRIMARY KEY,
    out_patient_no            TEXT,                    -- system-generated: 'ZH-OP-' || patient_id
    in_patient_no             TEXT,                    -- system-generated: 'ZH-IP-' || patient_id
    surname                   TEXT NOT NULL,
    other_names               TEXT NOT NULL,
    third_name                TEXT,
    sex                       TEXT NOT NULL CHECK (sex IN ('M', 'F')),
    date_of_birth             TIMESTAMPTZ,
    occupation                TEXT,
    residence                 TEXT,
    city_town                 TEXT,
    telephone1                TEXT,
    telephone2                TEXT,
    email_address             TEXT,
    postal_address            TEXT,
    postal_code               TEXT,
    next_of_kin               TEXT,
    next_of_kin_relationship  TEXT,
    next_of_kin_contact       TEXT,
    date_registered           TIMESTAMPTZ NOT NULL DEFAULT now(),
    id_type_id                INTEGER REFERENCES id_types(id_type_id),
    id_number                 TEXT,
    nationality_id            INTEGER REFERENCES nationalities(nationality_id),
    group_account_id          INTEGER REFERENCES group_accounts(group_account_id),
    reference_no              TEXT,
    principal_member          TEXT,      -- for dependents under a corporate/insurance account
    membership_no             TEXT,
    company_name              TEXT,
    note                      TEXT,
    registered_by             INTEGER REFERENCES system_users(system_user_id),

    CONSTRAINT patients_out_patient_no_unique UNIQUE (out_patient_no),
    CONSTRAINT patients_in_patient_no_unique UNIQUE (in_patient_no)
);

CREATE INDEX idx_patients_surname_othernames ON patients (surname, other_names);
CREATE INDEX idx_patients_out_patient_no ON patients (out_patient_no);
CREATE INDEX idx_patients_id_number ON patients (id_number);

-- ── Auto-generate OP number ──────────────────────────────────────────────
-- patient_id is only known once the row exists (SERIAL), so an AFTER INSERT
-- trigger fills this in right after the insert. COALESCE means an explicit
-- value passed in by the app (e.g. when migrating legacy records) is kept
-- instead of being overwritten.
--
-- in_patient_no is intentionally NOT generated here — it stays NULL until
-- the patient is actually admitted (a separate event, built in the
-- Admission module). See assign_inpatient_number() below, which the
-- Admission module will call when that module is built.

CREATE OR REPLACE FUNCTION assign_outpatient_number()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE patients
    SET out_patient_no = COALESCE(out_patient_no, 'ZH-OP-' || NEW.patient_id)
    WHERE patient_id = NEW.patient_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_assign_outpatient_number
AFTER INSERT ON patients
FOR EACH ROW
EXECUTE FUNCTION assign_outpatient_number();

-- Called by the future Admission module at the moment a patient is admitted
-- (not wired to any trigger yet — there's no admissions table to hang it off
-- of until that module exists).
CREATE OR REPLACE FUNCTION assign_inpatient_number(p_patient_id INTEGER)
RETURNS TEXT AS $$
DECLARE
    v_ip_no TEXT;
BEGIN
    UPDATE patients
    SET in_patient_no = COALESCE(in_patient_no, 'ZH-IP-' || p_patient_id)
    WHERE patient_id = p_patient_id
    RETURNING in_patient_no INTO v_ip_no;
    RETURN v_ip_no;
END;
$$ LANGUAGE plpgsql;

-- ── Module: OPD Visits ───────────────────────────────────────────────────
-- Source: tblclinics, tblmedicalinfos (via BaseClasses/_MedicalInfo.cs)

CREATE TABLE clinics (
    clinic_id   SERIAL PRIMARY KEY,
    name        TEXT NOT NULL
);

CREATE TABLE visits (
    visit_id          SERIAL PRIMARY KEY,
    patient_id        INTEGER NOT NULL REFERENCES patients(patient_id),
    clinic_id         INTEGER REFERENCES clinics(clinic_id),
    visit_datetime    TIMESTAMPTZ NOT NULL DEFAULT now(),
    age               INTEGER,          -- age snapshot at time of visit (years)
    age_months        INTEGER,          -- used for under-5 patients, per original MOH forms
    age_weeks         INTEGER,
    doctor            TEXT,             -- free text in the original app, not a FK
    nurse             TEXT,             -- free text in the original app, not a FK
    hpi               TEXT,             -- "History of Presenting Illness"
    summary           TEXT,
    is_processed      BOOLEAN NOT NULL DEFAULT FALSE,  -- true once billed
    is_admitted       BOOLEAN NOT NULL DEFAULT FALSE,
    is_consultant     BOOLEAN NOT NULL DEFAULT FALSE,  -- specialist consult vs regular OPD
    registered_by     INTEGER REFERENCES system_users(system_user_id)
);

CREATE INDEX idx_visits_patient_id ON visits (patient_id);
CREATE INDEX idx_visits_visit_datetime ON visits (visit_datetime);

-- ── Module: Billing ──────────────────────────────────────────────────────
-- Source: tblservices, tblmedicalbills, tblsaleitems (via BaseClasses)

CREATE TABLE services (
    service_id         SERIAL PRIMARY KEY,
    name               TEXT NOT NULL,
    department_id      INTEGER,          -- FK deferred until Departments module exists
    cash_rate          NUMERIC(14,2) NOT NULL DEFAULT 0,
    nhif_rate          NUMERIC(14,2),     -- original: NHIFFFS
    aar_rate           NUMERIC(14,2),     -- original: AAR
    kcb_rate           NUMERIC(14,2),     -- original: KCB
    eduafya_rate       NUMERIC(14,2),
    liason_rate        NUMERIC(14,2),
    national_scheme_rate NUMERIC(14,2),
    is_active          BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE medical_bills (
    medical_bill_id       SERIAL PRIMARY KEY,
    medical_bill_no       TEXT UNIQUE,       -- system-generated: ZH-MB-{medical_bill_id}
    visit_id              INTEGER REFERENCES visits(visit_id),
    patient_id            INTEGER REFERENCES patients(patient_id),
    is_patient            BOOLEAN NOT NULL DEFAULT TRUE,  -- false = walk-in cash sale, no patient record
    customer_name         TEXT,             -- snapshot at billing time (walk-in sales have no patient row)
    telephone_no          TEXT,
    id_number             TEXT,
    group_account_id      INTEGER REFERENCES group_accounts(group_account_id),
    total_bill_amount     NUMERIC(14,2) NOT NULL DEFAULT 0,
    sales_discount_amount NUMERIC(14,2) NOT NULL DEFAULT 0,
    write_off_amount      NUMERIC(14,2) NOT NULL DEFAULT 0,
    cover_amount          NUMERIC(14,2) NOT NULL DEFAULT 0,   -- portion billed to insurance/group account
    advance_payment       NUMERIC(14,2) NOT NULL DEFAULT 0,
    total_amount_paid     NUMERIC(14,2) NOT NULL DEFAULT 0,
    deposit_balance       NUMERIC(14,2) NOT NULL DEFAULT 0,
    deposit_offset        NUMERIC(14,2) NOT NULL DEFAULT 0,
    is_processed          BOOLEAN NOT NULL DEFAULT FALSE,   -- true once payment/finalization is done
    date_time_created     TIMESTAMPTZ NOT NULL DEFAULT now(),
    date_time_processed   TIMESTAMPTZ,
    processed_by          INTEGER REFERENCES system_users(system_user_id)
);

CREATE TABLE bill_items (
    bill_item_id        SERIAL PRIMARY KEY,
    medical_bill_id      INTEGER NOT NULL REFERENCES medical_bills(medical_bill_id) ON DELETE CASCADE,
    service_id           INTEGER REFERENCES services(service_id),
    name                 TEXT NOT NULL,     -- snapshot of service name at time of billing
    quantity              INTEGER NOT NULL DEFAULT 1,
    rate                  NUMERIC(14,2) NOT NULL DEFAULT 0,
    percentage_discount   NUMERIC(5,2) NOT NULL DEFAULT 0,
    discounted_amount     NUMERIC(14,2) NOT NULL DEFAULT 0,
    amount                NUMERIC(14,2) NOT NULL DEFAULT 0,  -- (rate * quantity) - discounted_amount
    has_been_paid_for     BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_medical_bills_visit_id ON medical_bills (visit_id);
CREATE INDEX idx_medical_bills_patient_id ON medical_bills (patient_id);
CREATE INDEX idx_bill_items_medical_bill_id ON bill_items (medical_bill_id);

-- Auto-generate the bill number, same pattern as OP numbers.
CREATE OR REPLACE FUNCTION assign_medical_bill_number()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE medical_bills
    SET medical_bill_no = COALESCE(medical_bill_no, 'ZH-MB-' || NEW.medical_bill_id)
    WHERE medical_bill_id = NEW.medical_bill_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_assign_medical_bill_number
AFTER INSERT ON medical_bills
FOR EACH ROW
EXECUTE FUNCTION assign_medical_bill_number();

-- ── Module: Admissions ───────────────────────────────────────────────────
-- Source: tblwards, tblbeds, tbladmissions, tbladmissionward

CREATE TABLE wards (
    ward_id     SERIAL PRIMARY KEY,
    name        TEXT NOT NULL
);

CREATE TABLE beds (
    bed_id      SERIAL PRIMARY KEY,
    ward_id     INTEGER NOT NULL REFERENCES wards(ward_id),
    bed_no      TEXT NOT NULL,
    bed_status  TEXT NOT NULL DEFAULT 'Vacant' CHECK (bed_status IN ('Vacant', 'Occupied')),
    UNIQUE (ward_id, bed_no)
);

CREATE TABLE admissions (
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

-- Bed assignment history — a patient can move beds/wards during one
-- admission, so this is a log, not a single column on admissions.
CREATE TABLE admission_ward (
    admission_ward_id  SERIAL PRIMARY KEY,
    admission_id        INTEGER NOT NULL REFERENCES admissions(admission_id),
    ward_id              INTEGER NOT NULL REFERENCES wards(ward_id),
    bed_id               INTEGER NOT NULL REFERENCES beds(bed_id),
    is_current_bed       BOOLEAN NOT NULL DEFAULT TRUE,
    assigned_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_admissions_patient_id ON admissions (patient_id);
CREATE INDEX idx_admissions_is_in_admission ON admissions (is_in_admission);
CREATE INDEX idx_admission_ward_admission_id ON admission_ward (admission_id);

-- Assigns in_patient_no the moment an admission is created — this is the
-- only place that happens (see assign_inpatient_number() above).
CREATE OR REPLACE FUNCTION on_admission_created()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM assign_inpatient_number(NEW.patient_id);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_on_admission_created
AFTER INSERT ON admissions
FOR EACH ROW
EXECUTE FUNCTION on_admission_created();

-- ── Optional starter data ───────────────────────────────────────────────
-- Uncomment and adjust to your context before running, or add via the app later.

-- INSERT INTO id_types (id_type) VALUES ('National ID'), ('Passport'), ('Birth Certificate');

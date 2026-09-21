-- Carepoint → Supabase (PostgreSQL) schema
-- Module: Patient Registration
--
-- Source of truth: extracted from the decompiled Carepoint 3.2 source
-- (tblpatients, tblgroupaccounts, tblnationality, tblidtypes, tblsystemusers).
-- Column names below are modernized to snake_case; the original MySQL
-- column name is noted in a comment where it differs.
--
-- Run this in the Supabase SQL Editor (Project -> SQL Editor -> New query).

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

    CONSTRAINT patients_out_patient_no_unique UNIQUE (out_patient_no)
);

CREATE INDEX idx_patients_surname_othernames ON patients (surname, other_names);
CREATE INDEX idx_patients_out_patient_no ON patients (out_patient_no);
CREATE INDEX idx_patients_id_number ON patients (id_number);

-- ── Optional starter data ───────────────────────────────────────────────
-- Uncomment and adjust to your context before running, or add via the app later.

INSERT INTO id_types (id_type) VALUES ('National ID'), ('Passport'), ('Birth Certificate');

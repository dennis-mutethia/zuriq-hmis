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
-- A lookup table rather than a hardcoded admin/staff pair, so adding a
-- role later (once the UI to create them exists) is just a row, not a
-- migration. is_admin_role is the only thing the app currently checks —
-- named roles beyond Admin/Staff are labels for now, not yet enforced
-- differently from each other (see README).
CREATE TABLE roles (
    role_id        SERIAL PRIMARY KEY,
    name           TEXT NOT NULL UNIQUE,
    is_admin_role  BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO roles (name, is_admin_role) VALUES
    ('Admin', TRUE),
    ('Staff', FALSE),
    ('Reception', FALSE),
    ('Pharmacy', FALSE),
    ('Clinical Officer', FALSE),
    ('Lab', FALSE);

CREATE TABLE system_users (
    system_user_id  SERIAL PRIMARY KEY,
    username         TEXT NOT NULL UNIQUE,
    password_hash    TEXT,             -- set by the app (werkzeug hash), never plaintext
    role_id          INTEGER NOT NULL REFERENCES roles(role_id),
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
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

-- ── Module: General Ledger (core of Accounts) ────────────────────────────
-- Source: tblaccounttypes, tblaccounts, tblsubaccounts, tblaccsubacc,
-- tbljournalvouchers, tblsubaccountentries. This is the double-entry
-- bookkeeping foundation — Bank Deposits/Reconciliation
-- (tblbankdeposits/tblbankrec) are a real, separate original module and
-- deliberately not built here; see README.
--
-- EntryType was a magic 0/1 int in the original (1 = Debit, per the
-- decompiled BaseClasses code) — modernized to a readable CHECK.

CREATE TABLE account_types (
    account_type_id  SERIAL PRIMARY KEY,
    name              TEXT NOT NULL UNIQUE
);

CREATE TABLE accounts (
    account_id       SERIAL PRIMARY KEY,
    account_no        TEXT NOT NULL UNIQUE,
    name               TEXT NOT NULL,
    account_type_id     INTEGER NOT NULL REFERENCES account_types(account_type_id)
);

-- Sub-accounts are the actual sub-ledgers (e.g. "Cash", "M-Pesa Till",
-- "NHIF Receivable") — each tagged under one or more control accounts via
-- account_sub_accounts, matching the original's separate junction table
-- rather than a direct FK (a sub-account can conceptually sit under more
-- than one account over time).
CREATE TABLE sub_accounts (
    sub_account_id   SERIAL PRIMARY KEY,
    name              TEXT NOT NULL
);

CREATE TABLE account_sub_accounts (
    acc_sub_acc_id   SERIAL PRIMARY KEY,
    account_id        INTEGER NOT NULL REFERENCES accounts(account_id),
    sub_account_id      INTEGER NOT NULL REFERENCES sub_accounts(sub_account_id),
    UNIQUE (account_id, sub_account_id)
);

CREATE TABLE fiscal_periods (
    fiscal_period_id  SERIAL PRIMARY KEY,
    name               TEXT NOT NULL,       -- e.g. 'January 2026'
    start_date          DATE NOT NULL,
    end_date             DATE NOT NULL,
    is_closed             BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE journal_vouchers (
    journal_voucher_id  SERIAL PRIMARY KEY,
    description           TEXT NOT NULL,
    transaction_datetime    TIMESTAMPTZ NOT NULL DEFAULT now(),
    source_reference          TEXT,          -- e.g. 'Bill ZH-MB-42' — free text link, not yet a real FK
    fiscal_period_id           INTEGER REFERENCES fiscal_periods(fiscal_period_id),
    created_by                   INTEGER REFERENCES system_users(system_user_id)
);

CREATE TABLE subaccount_entries (
    subaccount_entry_id  SERIAL PRIMARY KEY,
    journal_voucher_id     INTEGER NOT NULL REFERENCES journal_vouchers(journal_voucher_id) ON DELETE CASCADE,
    acc_sub_acc_id           INTEGER NOT NULL REFERENCES account_sub_accounts(acc_sub_acc_id),
    entry_type                 TEXT NOT NULL CHECK (entry_type IN ('Debit', 'Credit')),
    amount                       NUMERIC(14,2) NOT NULL CHECK (amount > 0),
    transaction_datetime           TIMESTAMPTZ NOT NULL DEFAULT now(),
    fiscal_period_id                 INTEGER REFERENCES fiscal_periods(fiscal_period_id)
);

CREATE INDEX idx_subaccount_entries_journal_voucher_id ON subaccount_entries (journal_voucher_id);
CREATE INDEX idx_subaccount_entries_acc_sub_acc_id ON subaccount_entries (acc_sub_acc_id);

INSERT INTO account_types (name) VALUES ('Asset'), ('Liability'), ('Equity'), ('Income'), ('Expense');

-- A minimal starting Chart of Accounts so payments have somewhere to post
-- to out of the box. This is a reasonable default for a small cash-pay
-- clinic, not a real accountant's chart — restructure freely via
-- /accounts/chart. The billing payment integration below looks these
-- sub-accounts up BY NAME, so renaming/deleting them turns off
-- auto-posting gracefully rather than breaking (see README).
INSERT INTO accounts (account_no, name, account_type_id) VALUES
    ('1000', 'Cash and Bank', (SELECT account_type_id FROM account_types WHERE name = 'Asset')),
    ('4000', 'Service Revenue', (SELECT account_type_id FROM account_types WHERE name = 'Income'));

INSERT INTO sub_accounts (name) VALUES ('Cash'), ('Service Revenue');

INSERT INTO account_sub_accounts (account_id, sub_account_id) VALUES
    ((SELECT account_id FROM accounts WHERE account_no = '1000'), (SELECT sub_account_id FROM sub_accounts WHERE name = 'Cash')),
    ((SELECT account_id FROM accounts WHERE account_no = '4000'), (SELECT sub_account_id FROM sub_accounts WHERE name = 'Service Revenue'));

-- ── Module: Queue Management ─────────────────────────────────────────────
-- Source: tbltempqueue. The original stores room names as free text and
-- waiting/service/total time as separately-stored integers (computed once,
-- never re-derived — can drift from the actual timestamps). Modernized:
-- rooms is a proper lookup table, and times are computed from timestamps
-- in the app layer rather than stored redundantly.

CREATE TABLE rooms (
    room_id    SERIAL PRIMARY KEY,
    name       TEXT NOT NULL UNIQUE
);

CREATE TABLE queue_entries (
    queue_entry_id  SERIAL PRIMARY KEY,
    visit_id          INTEGER NOT NULL REFERENCES visits(visit_id),
    from_room_id       INTEGER REFERENCES rooms(room_id),   -- null if this is their first stop
    to_room_id          INTEGER NOT NULL REFERENCES rooms(room_id),
    queued_at            TIMESTAMPTZ NOT NULL DEFAULT now(), -- joined this room's queue
    called_at             TIMESTAMPTZ,                        -- staff called them in
    completed_at           TIMESTAMPTZ,                        -- service finished, room freed
    created_by              INTEGER REFERENCES system_users(system_user_id)
);

CREATE INDEX idx_queue_entries_visit_id ON queue_entries (visit_id);
CREATE INDEX idx_queue_entries_to_room_id ON queue_entries (to_room_id);
CREATE INDEX idx_queue_entries_active ON queue_entries (to_room_id) WHERE completed_at IS NULL;

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

-- ── Module: Nursing / Vitals ─────────────────────────────────────────────
-- Source: tblnursetriage (OPD, one per visit), tblobservationcharts
-- (inpatient, repeated readings during an admission). These are two
-- distinct workflows in the original app, not one generic "vitals" table.
-- Placed here (after Admissions) because observation_charts depends on
-- the admissions table existing first.

CREATE TABLE nurse_triage (
    nurse_triage_id          SERIAL PRIMARY KEY,
    visit_id                   INTEGER NOT NULL REFERENCES visits(visit_id),
    blood_pressure              TEXT,             -- e.g. '120/80', kept as text to match free-entry format
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

CREATE INDEX idx_nurse_triage_visit_id ON nurse_triage (visit_id);

CREATE TABLE observation_charts (
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

CREATE INDEX idx_observation_charts_admission_id ON observation_charts (admission_id);

-- ── Module: Pharmacy / Dispensing ──────────────────────────────────────
-- Source: tblproducts, tblprescriptions, tblprescriptionitems
-- Note: the original schema has dozens of insurance-scheme price columns
-- on tblproducts (NHIF, AAR, KCB, Jubilee, Britam, ...). Deferred here,
-- same as the per-scheme rates on `services` — cash price only for now.

CREATE TABLE products (
    product_id         SERIAL PRIMARY KEY,
    code               TEXT,
    name               TEXT NOT NULL,
    description        TEXT,
    unit_definition    TEXT,          -- e.g. 'Tablet', 'Bottle', 'Vial'
    unit_cost          NUMERIC(14,2) NOT NULL DEFAULT 0,
    unit_price         NUMERIC(14,2) NOT NULL DEFAULT 0,
    quantity_in_stock  INTEGER NOT NULL DEFAULT 0,
    reorder_level      INTEGER NOT NULL DEFAULT 0,
    is_active          BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE prescriptions (
    prescription_id    SERIAL PRIMARY KEY,
    visit_id            INTEGER REFERENCES visits(visit_id),
    patient_id          INTEGER NOT NULL REFERENCES patients(patient_id),
    prescribed_by       TEXT,          -- doctor name, free text (matches visits.doctor)
    special_instruction TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE prescription_items (
    prescription_item_id  SERIAL PRIMARY KEY,
    prescription_id        INTEGER NOT NULL REFERENCES prescriptions(prescription_id) ON DELETE CASCADE,
    product_id              INTEGER REFERENCES products(product_id),
    inscription              TEXT NOT NULL,   -- snapshot of product name at prescribing time
    quantity                  INTEGER NOT NULL DEFAULT 1,
    quantity_per_time        TEXT,             -- e.g. '1 tablet'
    frequency_per_day        TEXT,             -- e.g. 'TDS', 'BD'
    dosage_duration          TEXT,             -- e.g. '5 days'
    other_instruction        TEXT,
    has_been_dispensed       BOOLEAN NOT NULL DEFAULT FALSE,
    dispensed_at             TIMESTAMPTZ
);

CREATE INDEX idx_prescriptions_visit_id ON prescriptions (visit_id);
CREATE INDEX idx_prescriptions_patient_id ON prescriptions (patient_id);
CREATE INDEX idx_prescription_items_prescription_id ON prescription_items (prescription_id);

-- Every change to quantity_in_stock — intake or dispensing — is logged
-- here. Without this, stock changes had zero audit trail: no record of
-- who received or dispensed what, or when.
CREATE TABLE suppliers (
    supplier_id      SERIAL PRIMARY KEY,
    name              TEXT NOT NULL,
    contact_person    TEXT,
    telephone         TEXT,
    email             TEXT,
    is_active         BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE stock_movements (
    stock_movement_id  SERIAL PRIMARY KEY,
    product_id           INTEGER NOT NULL REFERENCES products(product_id),
    supplier_id           INTEGER REFERENCES suppliers(supplier_id),  -- set on intake, null on dispensing
    quantity_change       INTEGER NOT NULL,   -- positive = received, negative = dispensed/adjusted out
    reason                 TEXT NOT NULL,      -- e.g. 'Stock intake', 'Dispensed — Rx #42'
    recorded_by            INTEGER REFERENCES system_users(system_user_id),
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_stock_movements_product_id ON stock_movements (product_id);
CREATE INDEX idx_stock_movements_supplier_id ON stock_movements (supplier_id);

-- ── Module: HR / Payroll ──────────────────────────────────────────────────
-- Source: tblemployees, tblpayrollparametercategories, tblpayrollparameters,
-- tblemployeepayrollparameter, tblpayslipperiods, tblpayslips,
-- tblemployeepayslipparameter.
--
-- IMPORTANT: the original computes full Kenyan statutory payroll (PAYE tax
-- bands, NHIF, NSSF, reliefs — tblpayslips has 30 columns for this). That
-- calculation logic is NOT reproduced here. Tax bands and statutory rates
-- change via legislation and this system has no way to know if they're
-- current — hardcoding them would risk silently miscalculating real
-- payroll. Instead: payroll_parameters lets you define any earning or
-- deduction (Basic Pay, House Allowance, PAYE, NHIF, NSSF, ...) and a
-- payslip is simple arithmetic: sum(Earnings) − sum(Deductions) = Net Pay.
-- You supply the actual statutory amounts (verified against current
-- KRA/NSSF/SHIF rates) as deduction parameters, same as any other
-- deduction. See README before running real payroll through this.

CREATE TABLE departments (
    department_id  SERIAL PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE
);

CREATE TABLE employment_types (
    employment_type_id  SERIAL PRIMARY KEY,
    name                  TEXT NOT NULL UNIQUE
);

CREATE TABLE employees (
    employee_id       SERIAL PRIMARY KEY,
    staff_no           TEXT UNIQUE,
    surname             TEXT NOT NULL,
    other_names           TEXT NOT NULL,
    id_type_id             INTEGER REFERENCES id_types(id_type_id),
    id_no                    TEXT,
    telephone1                TEXT,
    department_id              INTEGER REFERENCES departments(department_id),
    designation                  TEXT,
    employment_type_id             INTEGER REFERENCES employment_types(employment_type_id),
    date_employed                    DATE,
    payroll_no                         TEXT,
    pin_no                               TEXT,   -- KRA PIN
    nhif_no                               TEXT,
    nssf_no                                 TEXT,
    bank_name                                TEXT,   -- plain text for now — proper bank/branch
    bank_account_no                            TEXT,   -- normalization deferred to the Banking module
    is_active                                    BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE payroll_parameter_categories (
    parameter_category_id  SERIAL PRIMARY KEY,
    name                     TEXT NOT NULL,
    category_type              TEXT NOT NULL CHECK (category_type IN ('Earning', 'Deduction'))
);

CREATE TABLE payroll_parameters (
    payroll_parameter_id  SERIAL PRIMARY KEY,
    name                    TEXT NOT NULL,
    parameter_category_id     INTEGER NOT NULL REFERENCES payroll_parameter_categories(parameter_category_id)
);

-- An employee's standing/recurring parameters (e.g. their usual Basic Pay).
-- Payslips snapshot these at generation time into payslip_items, so
-- changing a standing amount never retroactively changes a past payslip.
CREATE TABLE employee_payroll_parameters (
    employee_payroll_parameter_id  SERIAL PRIMARY KEY,
    employee_id                      INTEGER NOT NULL REFERENCES employees(employee_id),
    payroll_parameter_id               INTEGER NOT NULL REFERENCES payroll_parameters(payroll_parameter_id),
    amount                                NUMERIC(14,2) NOT NULL DEFAULT 0,
    UNIQUE (employee_id, payroll_parameter_id)
);

CREATE TABLE payslip_periods (
    payslip_period_id  SERIAL PRIMARY KEY,
    pay_month            INTEGER NOT NULL CHECK (pay_month BETWEEN 1 AND 12),
    pay_year               INTEGER NOT NULL,
    beginning_date            DATE NOT NULL,
    ending_date                 DATE NOT NULL,
    UNIQUE (pay_month, pay_year)
);

CREATE TABLE payslips (
    payslip_id            SERIAL PRIMARY KEY,
    employee_id             INTEGER NOT NULL REFERENCES employees(employee_id),
    payslip_period_id         INTEGER NOT NULL REFERENCES payslip_periods(payslip_period_id),
    gross_earning_total         NUMERIC(14,2) NOT NULL DEFAULT 0,
    deduction_total               NUMERIC(14,2) NOT NULL DEFAULT 0,
    net_pay                         NUMERIC(14,2) NOT NULL DEFAULT 0,
    is_paid                           BOOLEAN NOT NULL DEFAULT FALSE,
    generated_at                       TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (employee_id, payslip_period_id)
);

-- Line-item snapshot for one payslip — name/type/amount copied at
-- generation time from employee_payroll_parameters (or entered directly
-- for a one-off adjustment), independent of later parameter changes.
CREATE TABLE payslip_items (
    payslip_item_id  SERIAL PRIMARY KEY,
    payslip_id         INTEGER NOT NULL REFERENCES payslips(payslip_id) ON DELETE CASCADE,
    name                 TEXT NOT NULL,
    category_type          TEXT NOT NULL CHECK (category_type IN ('Earning', 'Deduction')),
    amount                    NUMERIC(14,2) NOT NULL DEFAULT 0
);

CREATE INDEX idx_employees_department_id ON employees (department_id);
CREATE INDEX idx_employee_payroll_parameters_employee_id ON employee_payroll_parameters (employee_id);
CREATE INDEX idx_payslips_employee_id ON payslips (employee_id);
CREATE INDEX idx_payslips_payslip_period_id ON payslips (payslip_period_id);
CREATE INDEX idx_payslip_items_payslip_id ON payslip_items (payslip_id);

-- Reasonable starting set so the Employee form isn't empty on first use —
-- edit or add more via /hr/employment-types (admin only).
INSERT INTO employment_types (name) VALUES ('Permanent'), ('Contract'), ('Casual'), ('Part-time');

-- Category shells and one near-universal parameter (Basic Salary) — safe
-- to seed since these are just names, not statutory amounts. PAYE/NHIF/
-- NSSF are deliberately NOT seeded here (see the module comment above):
-- those need current, verified rates, and getting that wrong silently is
-- a real risk. Basic Salary carries no such risk — the amount is always
-- entered per employee regardless.
INSERT INTO payroll_parameter_categories (name, category_type) VALUES
    ('Earnings', 'Earning'),
    ('Deductions', 'Deduction');

INSERT INTO payroll_parameters (name, parameter_category_id) VALUES
    ('Basic Salary', (SELECT parameter_category_id FROM payroll_parameter_categories WHERE name = 'Earnings'));

-- ── Module: Lab ──────────────────────────────────────────────────────────
-- Source: tbltests, tblmedreqtests, tblmedreqtestitems
-- Note: the original also has tbltestcomponents (structured component-level
-- results with normal ranges/units, e.g. per-analyte reference ranges) but
-- nothing in the decompiled source links it to tblmedreqtestitems directly.
-- Deferred — results are free-text per test for now, not per-component.

CREATE TABLE tests (
    test_id     SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    specimen    TEXT,          -- e.g. 'Blood', 'Urine'
    cash_rate   NUMERIC(14,2) NOT NULL DEFAULT 0,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE lab_requests (
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

CREATE TABLE lab_request_items (
    lab_request_item_id  SERIAL PRIMARY KEY,
    lab_request_id         INTEGER NOT NULL REFERENCES lab_requests(lab_request_id) ON DELETE CASCADE,
    test_id                 INTEGER REFERENCES tests(test_id),
    test_name               TEXT NOT NULL,   -- snapshot of test name at request time
    conclusion               TEXT             -- the result, entered once done
);

CREATE INDEX idx_lab_requests_visit_id ON lab_requests (visit_id);
CREATE INDEX idx_lab_requests_patient_id ON lab_requests (patient_id);
CREATE INDEX idx_lab_request_items_lab_request_id ON lab_request_items (lab_request_id);

-- ── Optional starter data ───────────────────────────────────────────────
-- Uncomment and adjust to your context before running, or add via the app later.

-- INSERT INTO id_types (id_type) VALUES ('National ID'), ('Passport'), ('Birth Certificate');

-- A reasonable starting set of rooms for Queue Management — edit/add more via /queue/rooms.
INSERT INTO rooms (name) VALUES
    ('Reception'), ('Triage'), ('Consultation'), ('Lab'), ('Pharmacy'), ('Billing');

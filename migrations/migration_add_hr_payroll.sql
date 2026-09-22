-- Adds the HR/Payroll module. Does NOT compute Kenyan statutory payroll
-- (PAYE/NHIF/NSSF) — see the comment in schema.sql / README for why.
-- Requires id_types to already exist (base patient-registration schema).

BEGIN;

CREATE TABLE IF NOT EXISTS departments (
    department_id  SERIAL PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS employment_types (
    employment_type_id  SERIAL PRIMARY KEY,
    name                  TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS employees (
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
    pin_no                               TEXT,
    nhif_no                               TEXT,
    nssf_no                                 TEXT,
    bank_name                                TEXT,
    bank_account_no                            TEXT,
    is_active                                    BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS payroll_parameter_categories (
    parameter_category_id  SERIAL PRIMARY KEY,
    name                     TEXT NOT NULL,
    category_type              TEXT NOT NULL CHECK (category_type IN ('Earning', 'Deduction'))
);

CREATE TABLE IF NOT EXISTS payroll_parameters (
    payroll_parameter_id  SERIAL PRIMARY KEY,
    name                    TEXT NOT NULL,
    parameter_category_id     INTEGER NOT NULL REFERENCES payroll_parameter_categories(parameter_category_id)
);

CREATE TABLE IF NOT EXISTS employee_payroll_parameters (
    employee_payroll_parameter_id  SERIAL PRIMARY KEY,
    employee_id                      INTEGER NOT NULL REFERENCES employees(employee_id),
    payroll_parameter_id               INTEGER NOT NULL REFERENCES payroll_parameters(payroll_parameter_id),
    amount                                NUMERIC(14,2) NOT NULL DEFAULT 0,
    UNIQUE (employee_id, payroll_parameter_id)
);

CREATE TABLE IF NOT EXISTS payslip_periods (
    payslip_period_id  SERIAL PRIMARY KEY,
    pay_month            INTEGER NOT NULL CHECK (pay_month BETWEEN 1 AND 12),
    pay_year               INTEGER NOT NULL,
    beginning_date            DATE NOT NULL,
    ending_date                 DATE NOT NULL,
    UNIQUE (pay_month, pay_year)
);

CREATE TABLE IF NOT EXISTS payslips (
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

CREATE TABLE IF NOT EXISTS payslip_items (
    payslip_item_id  SERIAL PRIMARY KEY,
    payslip_id         INTEGER NOT NULL REFERENCES payslips(payslip_id) ON DELETE CASCADE,
    name                 TEXT NOT NULL,
    category_type          TEXT NOT NULL CHECK (category_type IN ('Earning', 'Deduction')),
    amount                    NUMERIC(14,2) NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_employees_department_id ON employees (department_id);
CREATE INDEX IF NOT EXISTS idx_employee_payroll_parameters_employee_id ON employee_payroll_parameters (employee_id);
CREATE INDEX IF NOT EXISTS idx_payslips_employee_id ON payslips (employee_id);
CREATE INDEX IF NOT EXISTS idx_payslips_payslip_period_id ON payslips (payslip_period_id);
CREATE INDEX IF NOT EXISTS idx_payslip_items_payslip_id ON payslip_items (payslip_id);

INSERT INTO employment_types (name) VALUES ('Permanent'), ('Contract'), ('Casual'), ('Part-time')
ON CONFLICT (name) DO NOTHING;

COMMIT;

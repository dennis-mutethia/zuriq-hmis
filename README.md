# Zuriq-HMIS → Flask: Patient Registration Module

First working module of the Carepoint rebuild — patient registration, backed
by Supabase (PostgreSQL).

## 1. Create the Supabase project

1. Go to [supabase.com](https://supabase.com) and create a new project (pick
   a region close to where the app will actually run).
2. Wait for provisioning to finish (a couple of minutes).

## 2. Create the schema

**New Supabase project (no tables yet):**
1. Open **SQL Editor -> New query**.
2. Paste in the contents of `schema.sql` and run it.
3. Check **Table Editor** — you should see `patients`, `group_accounts`,
   `nationalities`, `id_types`, and `system_users`.

**Already ran the earlier version of schema.sql (OP/IP numbers as integers)?**
Run `migration_op_ip_numbers.sql` instead — it converts the columns to text,
installs the auto-numbering trigger, and backfills any existing rows. Don't
run `schema.sql` again on top of an existing table.

4. Optional: add a row or two to `id_types` and `nationalities` so the
   dropdowns in the app aren't empty on first run — either via the Table
   Editor UI or by uncommenting the sample INSERT at the bottom of
   `schema.sql`.

### OP / IP numbers

`out_patient_no` and `in_patient_no` are system-generated — a database
trigger fills them in as soon as a patient row is inserted:

- `out_patient_no` → `ZH-OP-{patient_id}` (e.g. `ZH-OP-1042`)
- `in_patient_no` → `ZH-IP-{patient_id}` (e.g. `ZH-IP-1042`)

`out_patient_no` is not editable in the app — the registration form just
shows "Assigned automatically on save", and the edit form shows the
assigned value read-only. If you ever need to import legacy records with
their original numbers, insert with an explicit value for that column —
the trigger only fills it in when it's left `NULL`.

`in_patient_no` is deliberately **not** generated at registration — it
stays `NULL` for every patient until they're actually admitted. The
database has `assign_inpatient_number(patient_id)` ready for the Admission
module to call when that module is built; it's not wired to anything yet.

## 3. Get your connection string

1. In Supabase: **Project Settings -> Database -> Connection string -> URI**.
2. Use the **Transaction pooler** version (port `6543`) for normal app
   traffic — it's designed for exactly this (many short-lived connections
   from a web app).
3. Copy `.env.example` to `.env` and paste your connection string in as
   `DATABASE_URL`. Set `SECRET_KEY` to any random string.

## 4. Run the app locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Visit `http://localhost:5000/patients` — you should see an empty patient
list with a "Register Patient" button.

## What's implemented

**Patient Registration**
- Full CRUD (list with search, create, edit, delete)
- Dropdowns for ID Type, Nationality, and Group Account (billing account)
- OP number auto-generated as `ZH-OP-{patient_id}` on save (see below)

**OPD Visits** (`/visits`)
- Search for a patient, then record a visit against them (clinic, doctor,
  nurse, HPI, and whether it's a specialist consultation vs regular OPD)
- Patient's age/age-months/age-weeks is snapshotted automatically from their
  date of birth at the moment of the visit (matches the original app's
  under-5 vs adult distinction, used in Kenya MOH reporting forms)
- Visit list with search by patient name or OP number

**Billing** (`/billing`)
- Create a bill directly from a visit (service catalog with quantities,
  auto-calculated total)
- Bill number auto-generated as `ZH-MB-{medical_bill_id}` (same pattern as
  OP/IP numbers)
- Record payments against a bill; it's marked fully paid once the balance
  hits zero
- Simple service catalog admin (`/billing/services`) — add services with a
  cash rate; insurance/scheme rates exist in the schema but aren't in the
  form yet (see "deferred" below)
- Visit list shows a "Bill" shortcut once a visit hasn't been billed yet

If you're setting this up fresh, run `schema.sql` (it now includes all three
modules). If you already have Patients + Visits set up, run
`migrations/migration_add_billing.sql` to add just the billing tables.

## What's intentionally deferred (Billing)

- **Insurance/corporate billing** — `cover_amount`, and per-scheme rates on
  `services` (NHIF, AAR, KCB, etc.) exist in the schema but nothing in the
  app applies them yet; every bill today is treated as cash-pay.
- **Discounts and write-offs** — columns exist (`sales_discount_amount`,
  `write_off_amount`) but there's no UI for applying them.
- **Walk-in (non-patient) cash sales** — `medical_bills.is_patient` supports
  this, but the only flow built right now starts from a patient's visit.
- **Receipts** — no printable/PDF receipt yet, just the on-screen bill view.

## What's intentionally deferred

- **Authentication** — `system_users` is a stub table just so
  `patients.registered_by` has something to point at. Real login/roles is
  its own module (Security), not built yet. Right now the app has no login
  wall at all — don't put this on the open internet as-is.
- **Group Account business rules** (credit limits, co-pay, visit-day capping)
  — columns exist in the schema, but no logic enforces them yet. That
  belongs in the Billing module.
- **Blacklist / duplicate patient detection** — the original app has a
  `tblblacklistpatients` table and dedicate flows for this; not wired in yet.

## Suggested next module

Admissions — this is where `in_patient_no` finally gets assigned (via
`assign_inpatient_number()`, already sitting in the database waiting to be
called), and it's the other major branch off a visit besides billing.

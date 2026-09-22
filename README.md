# Zuriq-HMIS → Flask: Patient Registration Module

**Setting up a database?** See `MIGRATIONS.md` for the exact order to run
things in — there are 11+ migration files now and several depend on each
other. Fresh installs still just need `schema.sql`.

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

**Admissions** (`/admissions`)
- Admit a patient directly from a visit — pick a vacant bed (optional),
  admitting doctor, receiving nurse
- Assigns `in_patient_no` automatically the moment an admission is created
  (via `assign_inpatient_number()`, called by a DB trigger — this is the
  one and only place that happens)
- Discharge marks the admission ended and frees the bed
- Simple Wards & Beds admin (`/admissions/wards`) — add wards, add beds per
  ward, see live vacant/occupied status
- Bed assignment is tracked as a history (`admission_ward`), not a single
  column, since a patient can move beds/wards during one admission — this
  matters if you build ward-transfer later, but isn't exposed in the UI yet
- Visit list shows an "Admit" shortcut once a visit hasn't been admitted

Run `migrations/migration_add_admissions.sql` on an existing database (it
depends on `assign_inpatient_number()` already existing — run
`migration_op_ip_numbers.sql` first if you haven't). Fresh installs: just
run `schema.sql`, which now includes all four modules.

**Pharmacy / Dispensing** (`/pharmacy`)
- Create a prescription directly from a visit (multiple medications, each
  with quantity, frequency, and duration)
- Dispense line items individually — dispensing deducts from
  `products.quantity_in_stock` and blocks if there isn't enough on hand
- A prescription's status (Pending/Fully dispensed) reflects whether every
  item on it has been dispensed
- Simple product catalog admin (`/pharmacy/products`) with a low-stock
  indicator once quantity drops to the reorder level
- Visit list shows a "Prescribe" shortcut (always available — unlike
  Bill/Admit, a visit can have more than one prescription)

Run `migrations/migration_add_pharmacy.sql` on an existing database, or
`schema.sql` for a fresh install (now covers all five modules).

**Lab** (`/lab`)
- Request one or more tests from a visit (checkbox list against the test
  catalog)
- Enter results as free text per test, mark technologist, close out the
  request
- Simple test catalog admin (`/lab/tests`) with an optional specimen note
- Visit list shows a "Lab" shortcut (always available, same reasoning as
  Prescribe — a visit can have more than one lab request)

Run `migrations/migration_add_lab.sql` on an existing database, or
`schema.sql` for a fresh install (now covers all six modules).

## Roles

Roles live in their own `roles` table now (not a hardcoded text column),
seeded with **Admin, Staff, Reception, Pharmacy, Clinical Officer, Lab**.
This is groundwork for the real thing you'll eventually want — an admin
screen to create custom roles with specific permissions — without that
being built yet. Today, only one bit matters: `roles.is_admin_role`.
Everything else is a label.

Practically, that means:
- **Admin** unlocks the two actions that matter today (create users,
  delete patients) — see below
- **Staff, Reception, Pharmacy, Clinical Officer, Lab** are currently
  *identical* in what they can do — full access to every module. You can
  assign someone "Pharmacy" today for clarity in the Users list, but it
  doesn't yet restrict them to Pharmacy. That's the real feature (roles →
  permissions → enforcement) still ahead.

If you already ran the two-tier version of this from before, run
`migrations/migration_roles_table.sql` — it converts the old text column
to the new table and preserves existing admin/staff assignments. Fresh
installs: `schema.sql` already has the final shape.

In terms of actual enforced behavior, it's the smallest thing that closes
the two riskiest gaps that existed before:

- **Only admins can create new user accounts** (`/users/new`) — previously
  any logged-in user could
- **Only admins can delete a patient record** (destructive, no undo)

Everything else — registering patients, visits, billing, pharmacy, lab,
admissions, recording payments — stays open to any logged-in staff member,
since restricting those would make the app harder to use for no real
safety gain at this scale.

The "Users" section of the sidebar only appears for admins; a staff account
trying to reach `/users/new` directly gets redirected with a message
rather than a bare 403.

**Bootstrapping:** `flask create-admin` always creates an **admin** account
(there'd be no admin at all otherwise). Additional staff accounts go
through `/users` → "+ Add User" once an admin is logged in, with a role
picker on that form.

**If you already have users from before this change:** run
`migrations/migration_add_roles.sql`, then promote your own account:

```sql
UPDATE system_users SET role = 'admin' WHERE username = 'your-username';
```

Everyone else defaults to `staff`.

### What's intentionally deferred (Roles)

- **Granular permissions** — it's admin/staff, not a configurable matrix
  (e.g. "can record payments but not void them"). Fine for a small team,
  not fine at real scale.
- **Self-service role changes** — an admin can set a new user's role at
  creation time, but there's no "edit an existing user's role" screen yet;
  that's a direct-database change for now.
- **Per-module restrictions** — e.g. locking Pharmacy dispensing to actual
  pharmacy staff, or Lab results to lab techs. Everything staff-level is
  still all-or-nothing across every module.

## Reports

`/reports` — the "nice dashboards" you mentioned wanting eventually. Built
now rather than earlier because it needed real data flowing through
(bills, visits, stock) to be useful instead of decorative.

- **Revenue collected, last 30 days** — bar chart, grouped by day, from
  actual `total_amount_paid` on bills created each day
- **Visit volume, last 14 days** — line chart, from `visits`
- **Top outstanding bills** — the 10 largest unpaid balances, computed the
  same way `balance_due` is computed everywhere else in the app (total −
  paid − insurance cover), with a running total across all pending bills
- **Low stock products** — anything at or below its reorder level

Charts use Chart.js (CDN, no build step) styled to match the app's teal/ink
palette rather than default chart colors. This is a live query page, not a
cached report — it re-runs on every visit, which is fine at this scale but
worth revisiting if the bills/visits tables get very large later.

### What's intentionally deferred (Reports)

- **Date range picker** — the 30/14-day windows are hardcoded, not
  adjustable in the UI.
- **Export** — no CSV/PDF export of any report yet.
- **Per-clinic/per-doctor breakdowns** — everything here is facility-wide;
  no filtering by clinic, consultant, or payment method yet.

## HR — Employees & Payroll

Source: `tblemployees`, `tblemploymenttypes`, `tblpayrollparametercategories`,
`tblpayrollparameters`, `tblemployeepayrollparameter`, `tblpayslipperiods`,
`tblpayslips`, `tblemployeepayslipparameter`.

**This is genuinely dangerous territory to get wrong, so it's built
narrow and honest about it:** the original computes full Kenyan statutory
payroll (PAYE tax bands, NHIF, NSSF, reliefs — `tblpayslips` has 30 columns
for this). **That calculation logic is not reproduced here.** Tax bands
and statutory rates change via legislation, and this system has no way to
know if hardcoded rates are current — silently miscalculating someone's
real pay is a much worse failure mode than most bugs in this app. Instead:

- `/hr/parameters` — define any earning or deduction (Basic Pay, House
  Allowance, PAYE, NHIF, NSSF, ...) as a named parameter. **You supply the
  actual amounts, verified against current KRA/NSSF/SHIF guidance** — same
  as any other deduction, with a visible warning on that page saying so.
- `/hr` — add employees (staff no., ID, department, employment type, bank
  details) and set their standing payroll parameters (their usual Basic
  Pay, allowances, etc.)
- `/hr/payroll` — create a period (e.g. "January 2026"), then generate
  payslips: net pay is simple arithmetic, `sum(Earnings) − sum(Deductions)`,
  snapshotted from each employee's standing parameters at generation time
  — editing a standing amount later never retroactively changes a past
  payslip
- Generating a period's payslips skips anyone who already has one for that
  period, or who has no standing parameters set up yet — safe to re-run

No default employment types or payroll parameters are seeded — unlike
Rooms or Services elsewhere in this app, guessing at HR/payroll categories
felt more presumptuous than helpful here. Set up what your actual
organization uses via the UI.

Run `migrations/migration_add_hr_payroll.sql` on an existing database, or
`schema.sql` for fresh installs.

### What's intentionally deferred (HR)

- **Statutory payroll calculation** — see above; this is the load-bearing
  caveat of the whole module.
- **Payroll → GL posting** — payroll doesn't create journal vouchers
  (Debit Salary Expense, Credit Cash/Payable) yet; Accounts and HR are
  separate systems right now, same situation Billing was in before its
  own GL integration.
- **Bank/branch normalization** — `bank_name`/`bank_account_no` are plain
  text on Employee, not linked to the `tblbanks`/`tblbankbranch` structure
  from the original (which doesn't exist in Zuriq yet either — see Bank
  Deposits/Reconciliation under Accounts).
- **Leave, attendance, disciplinary records** — not part of this HR slice;
  the original likely has more HR forms beyond payroll not covered here.

## Billing → General Ledger integration

Recording a payment (`billing.record_payment`) now posts a journal voucher
automatically: **Debit Cash, Credit Service Revenue**, for the amount
received. This closes the gap flagged when the GL was first built — the
two systems were sitting side by side without talking.

**How it stays safe rather than becoming a hard dependency:** the posting
looks up two sub-accounts *by name* — `Cash` and `Service Revenue` — seeded
by default (see below). If you rename or delete either one while
restructuring your Chart of Accounts, payments still record fine; the GL
posting is silently skipped and the flash message tells you so
("GL posting skipped — default Cash/Service Revenue accounts not found").
A payment must always be recordable even if the books aren't set up.

**This is a deliberately minimal default, not real accounting advice** —
one cash account, one revenue account, no differentiation between OPD
consultation revenue vs pharmacy revenue vs lab revenue, no accounts
receivable entry for insurance/credit sales. It's enough to prove the
integration works and give you a real running Cash ledger
(`/accounts/ledger/<id>` on the Cash sub-account shows every payment ever
recorded). Restructure the Chart of Accounts to match how your business
actually wants to track revenue whenever you're ready — the posting logic
will follow whatever you name `Cash` and `Service Revenue` as, or you can
edit `_post_payment_to_gl()` in `app/routes/billing.py` for anything more
specific (e.g. separate revenue accounts per module).

Run `migrations/migration_seed_default_accounts.sql` on an existing
database (safe to run even if you've already customized your accounts —
it only creates what's missing). Fresh installs: `schema.sql` seeds it
already.

## Accounts — General Ledger (core)

Source: `tblaccounttypes`, `tblaccounts`, `tblsubaccounts`, `tblaccsubacc`,
`tbljournalvouchers`, `tblsubaccountentries`. This is real double-entry
bookkeeping, not a simplification — the original's own structure already
separates a chart of accounts (control accounts) from sub-accounts (actual
ledgers like "Cash" or "M-Pesa Till"), linked via a junction table so a
sub-account isn't hardcoded to one control account.

**One thing modernized rather than copied exactly:** `EntryType` was a
magic `0`/`1` integer in the original (1 = Debit, found by reading the
actual comparison logic in the decompiled BaseClasses — nothing in the
schema itself said which was which). Replaced with a readable
`CHECK (entry_type IN ('Debit', 'Credit'))`.

**Setup order** (this module has real dependencies you must set up before
it's usable):
1. **Chart of Accounts** (`/accounts/chart`) — add control accounts (e.g.
   `1000 — Current Assets`, type `Asset`)
2. **Sub-Accounts** (`/accounts/sub-accounts`) — add actual ledgers (e.g.
   `Cash`, `M-Pesa Till`), then **link** each to a Chart of Accounts entry
3. **New Journal Voucher** (`/accounts`) — post an entry: description,
   optional reference, and at least one debit line + one credit line.
   **Debits must equal credits or it won't save** — this is checked in
   the route, not just the UI.
4. **Ledger view** — from any sub-account, see every entry against it with
   a running balance

**Fiscal periods are automatic** — `FiscalPeriod.get_or_create_current()`
finds or creates the current calendar-month period the first time you post
a voucher in it. No manual period setup needed, though `/accounts/periods`
shows the history.

Run `migrations/migration_add_general_ledger.sql` on an existing database,
or `schema.sql` for fresh installs (both seed the five account types:
Asset, Liability, Equity, Income, Expense).

### What's intentionally deferred (Accounts)

- **Bank Deposits & Reconciliation** — `tblbankdeposits`/`tblbankrec` are a
  real, separate original module (matching a bank statement against book
  balances) and genuinely weren't built here. This GL core is the
  foundation it would sit on top of.
- **Only payments post automatically, and only at a single-account level**
  — see "Billing → General Ledger integration" below. Pharmacy dispensing
  and Lab results still don't post their own entries (e.g. cost-of-goods
  for dispensed drugs), and there's no per-module revenue split (OPD vs
  Pharmacy vs Lab all land in one "Service Revenue" account today).
- **Closing periods** — `fiscal_periods.is_closed` exists but nothing sets
  it or blocks entries into a closed period.
- **Trial balance / financial statements** — the original has dedicated
  reports for this (`tbltrialbalance` referenced in the decompiled source);
  not built. The per-sub-account ledger view is the closest equivalent
  right now.
- **HR/Payroll's own accounting** — `tblemployeepayrollparameter` etc. are
  a separate untouched module; this GL core doesn't post payroll entries.

## Queue Management

Source: `tbltempqueue`. Modernized two things rather than copying the
original structure exactly:

- **Rooms are a proper lookup table**, not free text — the original
  stored `FromRoom`/`ToRoom` as plain strings, which means two staff
  members typing "Lab" vs "lab" would never match in a report.
- **Wait/service times are computed from timestamps**, not stored as
  separate integers — the original calculated `WaitingTime`/`ServiceTime`
  once and stored them, which can silently go stale. Here they're derived
  live from `queued_at`/`called_at`/`completed_at` every time they're
  shown.

**`/queue`** — the live board: every room as a column, patients currently
waiting or in service, with "Call In" and "Mark Done" actions. **"Queue"**
from the Visits list sends a patient to a specific room's line — it
tracks which room they came from automatically (their previous stop),
building an implicit trail of where they've been today. `/queue/rooms` —
simple admin to add rooms; six are seeded by default (Reception, Triage,
Consultation, Lab, Pharmacy, Billing).

Run `migrations/migration_add_queue.sql` on an existing database, or
`schema.sql` for fresh installs (both seed the default rooms).

### What's intentionally deferred (Queue)

- **Multi-branch/multi-room-type routing rules** — no logic suggesting
  "where should this patient go next"; staff pick manually every time.
- **Queue analytics** — no average-wait-time reporting yet; the per-entry
  minutes shown on the board aren't aggregated anywhere in Reports.

## Nursing / Vitals

The original app has two distinct workflows here, not one generic "vitals"
table — kept them separate rather than merging them into something simpler
but less faithful:

- **Nurse Triage** (`/nursing`, or "Triage" from the Visits list) — one
  record per OPD visit: blood pressure, pulse, respiration, temperature,
  weight, each with its own remarks field, plus general notes. This is
  what happens between registration and seeing the doctor.
- **Observation Chart** (`/nursing/admission/<id>`, or "Vitals" from
  Admissions) — repeated readings over time during an inpatient stay:
  systolic/diastolic BP, pulse, respiratory rate, SPo2, temperature. Unlike
  triage, this is a running log, not a single record — the page shows
  entry form + full reading history together.

Before this, Zuriq had zero structured clinical documentation beyond a
single free-text HPI field on Visit. This is the first real clinical data
capture beyond "a visit happened."

Run `migrations/migration_add_nursing.sql` on an existing database, or
`schema.sql` for fresh installs.

### What's intentionally deferred (Nursing)

- **Nurse Care Plans** — the original has a separate care-planning
  workflow (`tblnursecareplan`) not built here; triage and observation
  charts cover vitals capture, not care planning.
- **Reference ranges / abnormal flagging** — no automatic highlighting of
  out-of-range vitals (e.g. a dangerously low SPo2) yet.

## Billing links (Pharmacy + Lab → Billing)

Dispensing a medication or completing a lab test now generates a real bill
line automatically, instead of needing manual re-entry in Billing:

- **Dispensing** a prescription item adds `Product Name x{quantity}` to the
  visit's bill at `product.unit_price × quantity`
- **Saving lab results** adds each completed test to the visit's bill at
  `test.cash_rate` — this is why tests now have a cash rate (they didn't
  before; see `migrations/migration_billing_links.sql`)
- All three sources — OPD services, Pharmacy, Lab — now bill into **the
  same running bill per visit** rather than each starting a separate one.
  `MedicalBill.get_or_create_for_visit()` finds the visit's existing unpaid
  bill and adds to it, or starts one if none exists yet. This also fixed a
  latent issue in the original Billing flow: clicking "Bill" on a visit
  more than once used to create duplicate bills for the same visit — now
  it correctly adds to the one open bill instead.
- If a prescription or lab request isn't tied to a visit (nullable by
  design — matches the original schema's support for self-requests /
  walk-ins), nothing gets billed automatically; that stays a manual
  Billing entry for now.

Run `migrations/migration_billing_links.sql` on an existing database (adds
`tests.cash_rate` — safe to run even if you already have `tests` and
`bill_items` from earlier migrations). Fresh installs: `schema.sql` already
includes it.

### What's intentionally deferred (Billing links)

- **Editing/removing an auto-billed item** — once dispensing or a lab
  result adds a line, there's no undo in the UI; fixing a mistake means
  editing the database directly.
- **Discounts/insurance on dispensed or lab items** — they bill at full
  cash rate; the discount/cover-amount logic that exists on `medical_bills`
  isn't applied automatically to these lines.

## Authentication

Every page now requires login — `system_users` is no longer a stub.

**Bootstrap your first login** (run this once, from the terminal, after
applying `migration_add_auth.sql` or the updated `schema.sql`):

```bash
flask create-admin
```

It'll prompt for a username and password and hash it correctly. From then
on, log in at `/login`, and add more staff accounts either the same way or
through the app at `/users` → "+ Add User".

Passwords are hashed with Werkzeug's `generate_password_hash` (never stored
in plain text). Sessions are Flask's signed-cookie sessions, keyed off
`SECRET_KEY` in your `.env` — make sure that's a real random value in
production, not the `dev-secret-change-me` default.

### What's intentionally deferred (Auth)

- **Roles/permissions** — there's only one tier: logged in or not. Any user
  can create another user, discharge a patient, void a bill, everything.
  Fine for a small trusted team; add role checks before this scales up or
  handles anything you wouldn't want every staff member touching.
- **Password reset / email** — none. If someone forgets their password,
  another logged-in user (or you, via the database) has to set a new one.
- **Account deactivation from the UI** — `is_active` exists on the model
  and is enforced at login, but there's no button to flip it yet; do it
  directly in the database for now.
- **Audit trail** — logins aren't logged anywhere yet, and actions
  (registered_by, processed_by, etc.) already reference `system_users` but
  nothing surfaces "who did what" in the UI.

## What's intentionally deferred (Lab)

- **Structured component-level results** — the original app has a
  `tbltestcomponents` table for per-analyte results with normal ranges and
  units (e.g. Hemoglobin: 12–16 g/dL), but nothing in the decompiled source
  links it to individual test requests. Results here are free text per
  test, not per component.
- **Reference ranges / flagging abnormal results** — no automatic
  high/low flagging yet, since there's no structured range data wired in.

## Stock Intake & Movement Ledger

Stock could previously only go down (dispensing) — there was no way to
receive new stock except editing the database directly, which meant the
module would eventually stop working once initial stock ran out. Fixed:

- **`/pharmacy/products/<id>/receive`** — add received stock with an
  optional note (supplier/invoice reference)
- **Every stock change is now logged** — `stock_movements` records
  quantity, reason, who did it, and when, for both intake and dispensing
  (dispensing wasn't logged anywhere before this either)
- **`/pharmacy/products/<id>/history`** — the ledger for a single product

A `suppliers` table now exists too — the intake form has a supplier
dropdown ("Add a supplier" inline if the one you need isn't listed yet),
and each stock movement records which supplier it came from. This is
intentionally *not* a full purchase-order/GRN workflow — no PO numbers,
no cost reconciliation, no approval flow. It's the minimum needed to keep
the Pharmacy module actually usable over time and to know where stock
came from.

Run these on an existing database, in order:
`migrations/migration_add_stock_movements.sql`, then
`migrations/migration_add_suppliers.sql`. Fresh installs: `schema.sql`
already has both.

## What's intentionally deferred (Pharmacy)

- **Insurance/scheme drug pricing** — the original app has ~20 per-insurer
  price columns on the product table (NHIF, AAR, Britam, Jubilee, etc.);
  only a single cash price exists here for now, same simplification as
  Services in Billing.
- **Purchase orders** — suppliers exist and are linked to intake now, but
  there's no PO/GRN workflow — no order placed, expected, or reconciled
  against what actually arrived. Intake is still a manual quantity entry.

## What's intentionally deferred (Admissions)

- **Ward transfers** — the schema supports a patient moving beds mid-admission
  (`admission_ward` is a history, not a single column) but there's no UI for
  it yet; only the initial bed assignment at admission time is wired in.
- **Inpatient billing** — admissions don't yet generate their own bills
  (deposits, daily bed charges); the existing Billing module only bills OPD
  visits directly.

## Suggested next module

Every gap flagged as a real risk (no login, no billing links, no roles) is
now closed. What's left in the "deferred" notes throughout this README is
genuine feature depth, not safety gaps — insurance/scheme pricing, ward
transfers, structured lab results, password reset, and so on. Worth
picking based on what actually gets used, not building further ahead of
real usage.

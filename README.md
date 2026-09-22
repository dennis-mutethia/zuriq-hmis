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

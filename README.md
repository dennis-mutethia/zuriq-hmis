# Carepoint → Flask: Patient Registration Module

First working module of the Carepoint rebuild — patient registration, backed
by Supabase (PostgreSQL).

## 1. Create the Supabase project

1. Go to [supabase.com](https://supabase.com) and create a new project (pick
   a region close to where the app will actually run).
2. Wait for provisioning to finish (a couple of minutes).

## 2. Create the schema

1. In your Supabase project, open **SQL Editor -> New query**.
2. Paste in the contents of `schema.sql` (in this folder) and run it.
3. Check **Table Editor** — you should see `patients`, `group_accounts`,
   `nationalities`, `id_types`, and `system_users`.
4. Optional: add a row or two to `id_types` and `nationalities` so the
   dropdowns in the app aren't empty on first run — either via the Table
   Editor UI or by uncommenting the sample INSERT at the bottom of
   `schema.sql`.

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

- Full CRUD for patient registration (list with search, create, edit, delete)
- Dropdowns for ID Type, Nationality, and Group Account (billing account),
  matching the original app's patient registration form fields
- Tailwind-based modern styling (via CDN — no build step needed)

## What's intentionally deferred

- **Authentication** — `system_users` is a stub table just so
  `patients.registered_by` has something to point at. Real login/roles is
  its own module (Security), not built yet. Right now the app has no login
  wall at all — don't put this on the open internet as-is.
- **OP number auto-assignment** — the original app likely has specific
  sequencing/formatting rules for OutPatientNo (worth checking the real app's
  behavior before relying on the manual entry field here).
- **Group Account business rules** (credit limits, co-pay, visit-day capping)
  — columns exist in the schema, but no logic enforces them yet. That
  belongs in the Billing module.
- **Blacklist / duplicate patient detection** — the original app has a
  `tblblacklistpatients` table and dedicate flows for this; not wired in yet.

## Suggested next module

OPD Visit / Queue — the natural next step after a patient exists, and it's
what most other modules (billing, lab, consultations) hang off of.

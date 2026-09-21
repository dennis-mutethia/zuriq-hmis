# Zuriq 1.0 → Flask Migration: Codebase Analysis

Generated from the ILSpy decompilation of `Carepoint 3.2.exe` (2,031 C# files,
282 form resource files, 261 Crystal Reports files).

## Architecture found

The app is layered, not just WinForms code-behind spaghetti:

- **BaseClasses / DerivedClasses** — business object classes (e.g. `_Patient.cs`)
- **Collections / DerivedCollections** — typed collections of those objects
- **DataSets** — ADO.NET typed DataSets, each with a **TableAdapter** that embeds
  real, complete SQL (MySQL) as plain strings — this is what made schema
  extraction possible without live DB access
- **Forms** — WinForms UI (299 form code-behind files across ~15 module folders)
- **Reports** — Crystal Reports code-behind (261 `.rpt` files — binary format,
  will need to be rebuilt as HTML/PDF templates one by one; report *names* are
  known, contents are not yet)

## What's in this folder

- **typed_schema.md** — 179 DataTable classes, 3,242 columns, each with its
  real .NET type (string/int/DateTime/double/etc.), pulled from the typed
  DataSet designer code.
- **inferred_schema.md** — 182 distinct MySQL tables (`tblpatients`,
  `tbladmissions`, `tblarinvoices`, etc.) with best-effort column lists,
  pulled from the actual SQL text in TableAdapters. This is how we recover
  real table names even though typed_schema.md's class names don't always
  match them 1:1.
- **carepoint_extracted_sql.json** — all 423 raw SQL statements found in the
  code, each tagged with its source file. Useful for cross-checking specific
  queries when we get to a given module.
- **tables_summary.txt** — quick one-line-per-table index.

These two schema docs aren't a perfect DDL dump (no indexes, foreign keys, or
constraints — those live in the database, not the code), but together they
cover the large majority of what a rebuild needs to define models correctly.

## Module map (by form count)

| Module folder | Forms (approx.) |
|---|---|
| Accounts (billing, AR, GL, banking) | 58+ |
| InPatient (admissions, vitals, wards) | 30 |
| Procurement (POs, GRNs, suppliers) | 15 |
| HR (payroll, employees) | 14 |
| Core Forms (patients, queue, main menu, etc.) | ~126 |
| Reports forms (report option dialogs) | 19 |

Patient registration/records sit in the **core Forms** folder and
**PatientDataSets** — not siloed into their own module folder, which makes
sense since nearly every other module (billing, admissions, lab) references
`tblpatients`.

## Recommended first module: Patient Registration + OPD Visit

This is the natural starting point because:
- It's the most self-contained table cluster (`tblpatients`,
  `tblgroupaccounts`, `tblnationality`, `tblidtypes` — all in
  **inferred_schema.md**)
- Nearly every other module has a foreign key into it, so getting this right
  first makes every later module easier
- We already have the real SQL and typed columns for it (see
  `dTPatientRegTableAdapter` in the SQL dump)

## Suggested next step

Build the Flask + SQLAlchemy models and basic CRUD screens for Patient
Registration first, using the schema docs above as ground truth, then
validate against how patient registration actually works in the real
clinic before moving to the next module (likely OPD visits/queue, since
that's the next thing that happens to a patient after registration).

# Migration Order

**Fresh Supabase project, nothing set up yet:** ignore everything below —
just run `schema.sql` once in the SQL Editor. It contains the final shape
of every table, already in a valid creation order (verified: every foreign
key references a table created earlier in the same file). Done.

**Existing database, catching up:** run these in exact order. Skip any
you've already applied, but don't skip ahead — several depend on the one
before it.

| # | File | Depends on | Adds |
|---|------|-----------|------|
| 1 | `migration_op_ip_numbers.sql` | `patients` table already exists | OP/IP number auto-generation |
| 2 | `migration_add_visits.sql` | #1 | `clinics`, `visits` |
| 3 | `migration_add_billing.sql` | #2 | `services`, `medical_bills`, `bill_items` |
| 4 | `migration_add_admissions.sql` | #1, #2 | `wards`, `beds`, `admissions`, `admission_ward` |
| 5 | `migration_add_pharmacy.sql` | #2 | `products`, `prescriptions`, `prescription_items` |
| 6 | `migration_add_lab.sql` | #2 | `tests`, `lab_requests`, `lab_request_items` |
| 7 | `migration_add_auth.sql` | `system_users` table already exists | `password_hash`, `is_active` on `system_users` |
| 8 | `migration_billing_links.sql` | #6 | `cash_rate` on `tests` |
| 9 | `migration_roles_table.sql` | #7 | `roles` table + `system_users.role_id` |
| 10 | `migration_add_stock_movements.sql` | #5 | `stock_movements` |
| 11 | `migration_add_suppliers.sql` | #10 | `suppliers`, links to `stock_movements` |
| 12 | `migration_add_nursing.sql` | #2, #4 | `nurse_triage`, `observation_charts` |
| 13 | `migration_add_queue.sql` | #2 | `rooms`, `queue_entries` (seeds 6 default rooms) |
| 14 | `migration_add_general_ledger.sql` | `system_users` table already exists | `account_types`, `accounts`, `sub_accounts`, `account_sub_accounts`, `fiscal_periods`, `journal_vouchers`, `subaccount_entries` (seeds 5 account types) |
| 15 | `migration_seed_default_accounts.sql` | #14 | Default `Cash`/`Service Revenue` accounts, used by the Billing payment integration |

**Skip `migration_add_roles.sql` entirely** if you haven't already run it —
`migration_roles_table.sql` (step 9) supersedes it and does the equivalent
setup directly with the final table structure. If you *did* already run
`migration_add_roles.sql` before this document existed, that's fine —
step 9 detects and converts it automatically.

After step 9, if this is the first time roles exist on this database,
promote yourself:
```sql
UPDATE system_users SET role_id = (SELECT role_id FROM roles WHERE name = 'Admin')
WHERE username = 'your-username';
```

## Checking where you are

Not sure what you've already run? In the Supabase SQL Editor:
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY 1;
```
Compare against the "Adds" column above — whichever tables are missing
tells you which migration to run next.

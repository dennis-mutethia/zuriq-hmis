-- Adds a cash rate to tests (needed so completed lab tests can generate a
-- bill line — there was no price on tests until now) and prepares for
-- Pharmacy/Lab to bill into the same running bill as OPD services.
-- No other schema change is needed: bill_items already stores a name/
-- quantity/rate/amount snapshot without requiring a service_id, so
-- pharmacy- and lab-originated lines fit the existing table as-is.

BEGIN;

ALTER TABLE tests ADD COLUMN IF NOT EXISTS cash_rate NUMERIC(14,2) NOT NULL DEFAULT 0;

COMMIT;

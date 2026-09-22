-- Seeds a minimal default Chart of Accounts (Cash and Bank / Service
-- Revenue) so the Billing → GL payment integration has somewhere to post
-- to. Requires migration_add_general_ledger.sql to already be applied.
-- Safe to run even if you've already customized your accounts — uses
-- ON CONFLICT / existence checks so it won't create duplicates.

BEGIN;

INSERT INTO accounts (account_no, name, account_type_id)
SELECT '1000', 'Cash and Bank', (SELECT account_type_id FROM account_types WHERE name = 'Asset')
WHERE NOT EXISTS (SELECT 1 FROM accounts WHERE account_no = '1000');

INSERT INTO accounts (account_no, name, account_type_id)
SELECT '4000', 'Service Revenue', (SELECT account_type_id FROM account_types WHERE name = 'Income')
WHERE NOT EXISTS (SELECT 1 FROM accounts WHERE account_no = '4000');

INSERT INTO sub_accounts (name)
SELECT 'Cash' WHERE NOT EXISTS (SELECT 1 FROM sub_accounts WHERE name = 'Cash');

INSERT INTO sub_accounts (name)
SELECT 'Service Revenue' WHERE NOT EXISTS (SELECT 1 FROM sub_accounts WHERE name = 'Service Revenue');

INSERT INTO account_sub_accounts (account_id, sub_account_id)
SELECT (SELECT account_id FROM accounts WHERE account_no = '1000'),
       (SELECT sub_account_id FROM sub_accounts WHERE name = 'Cash')
WHERE NOT EXISTS (
    SELECT 1 FROM account_sub_accounts
    WHERE account_id = (SELECT account_id FROM accounts WHERE account_no = '1000')
      AND sub_account_id = (SELECT sub_account_id FROM sub_accounts WHERE name = 'Cash')
);

INSERT INTO account_sub_accounts (account_id, sub_account_id)
SELECT (SELECT account_id FROM accounts WHERE account_no = '4000'),
       (SELECT sub_account_id FROM sub_accounts WHERE name = 'Service Revenue')
WHERE NOT EXISTS (
    SELECT 1 FROM account_sub_accounts
    WHERE account_id = (SELECT account_id FROM accounts WHERE account_no = '4000')
      AND sub_account_id = (SELECT sub_account_id FROM sub_accounts WHERE name = 'Service Revenue')
);

COMMIT;

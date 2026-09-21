-- Replaces the admin/staff CHECK-constrained text column (added by
-- migration_add_roles.sql) with a proper roles lookup table, so adding a
-- new role later is a row insert, not a schema migration. Safe to run
-- whether or not you already applied migration_add_roles.sql — this
-- supersedes it.

BEGIN;

CREATE TABLE IF NOT EXISTS roles (
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
    ('Lab', FALSE)
ON CONFLICT (name) DO NOTHING;

ALTER TABLE system_users ADD COLUMN IF NOT EXISTS role_id INTEGER REFERENCES roles(role_id);

-- Backfill from the old text `role` column, if this database has it
-- (i.e. you ran migration_add_roles.sql before this one).
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'system_users' AND column_name = 'role'
    ) THEN
        UPDATE system_users su
        SET role_id = r.role_id
        FROM roles r
        WHERE su.role_id IS NULL AND lower(su.role) = lower(r.name);

        ALTER TABLE system_users DROP CONSTRAINT IF EXISTS system_users_role_check;
        ALTER TABLE system_users DROP COLUMN role;
    END IF;
END $$;

-- Anyone still without a role (e.g. rows that predate roles entirely)
-- defaults to Staff, not Admin — never widen access silently.
UPDATE system_users
SET role_id = (SELECT role_id FROM roles WHERE name = 'Staff')
WHERE role_id IS NULL;

ALTER TABLE system_users ALTER COLUMN role_id SET NOT NULL;

COMMIT;

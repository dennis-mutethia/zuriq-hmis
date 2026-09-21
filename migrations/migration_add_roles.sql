-- Adds a two-tier role (admin / staff) to system_users. Existing users
-- default to 'staff' — promote your own account to 'admin' manually after
-- running this (see the UPDATE below), since nothing here can know which
-- existing user should be the admin.

BEGIN;

ALTER TABLE system_users
    ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'staff';

ALTER TABLE system_users
    ADD CONSTRAINT system_users_role_check CHECK (role IN ('admin', 'staff'));

COMMIT;

-- Run this once, with your own username, to promote yourself to admin:
--   UPDATE system_users SET role = 'admin' WHERE username = 'your-username';

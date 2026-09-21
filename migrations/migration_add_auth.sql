-- Adds real authentication fields to system_users, which has been a stub
-- table (just an id and username) until now.

BEGIN;

ALTER TABLE system_users ADD COLUMN IF NOT EXISTS password_hash TEXT;
ALTER TABLE system_users ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;

COMMIT;

-- After running this, bootstrap your first login from the terminal:
--   flask create-admin
-- (it will prompt for a username and password and hash it correctly —
-- never insert a plaintext password directly into password_hash).

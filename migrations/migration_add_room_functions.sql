-- Adds a `function` tag to rooms so Nursing/Consultation/Lab (and future
-- screens) can show and act on their own queue directly, instead of only
-- seeing "everyone in-service everywhere" as before. NULL means a
-- general-purpose room with no specific screen attached.

BEGIN;

ALTER TABLE rooms ADD COLUMN IF NOT EXISTS function TEXT;
ALTER TABLE rooms ADD CONSTRAINT rooms_function_check
    CHECK (function IN ('triage', 'consultation', 'lab', 'pharmacy', 'billing', 'reception'));

-- Best-effort auto-tagging by existing room name, since most installs
-- will have used the seeded default names. Silently does nothing for
-- rooms with other names — tag those manually via /queue/rooms.
UPDATE rooms SET function = 'reception'    WHERE lower(name) = 'reception'    AND function IS NULL;
UPDATE rooms SET function = 'triage'       WHERE lower(name) = 'triage'       AND function IS NULL;
UPDATE rooms SET function = 'consultation' WHERE lower(name) = 'consultation' AND function IS NULL;
UPDATE rooms SET function = 'lab'          WHERE lower(name) = 'lab'          AND function IS NULL;
UPDATE rooms SET function = 'pharmacy'     WHERE lower(name) = 'pharmacy'     AND function IS NULL;
UPDATE rooms SET function = 'billing'      WHERE lower(name) = 'billing'      AND function IS NULL;

COMMIT;

-- Adds Queue Management: rooms + queue_entries. Modernized from the
-- original tbltempqueue — rooms is a lookup table (not free text), and
-- wait/service times are computed from timestamps, not stored as
-- separate integers.

BEGIN;

CREATE TABLE IF NOT EXISTS rooms (
    room_id    SERIAL PRIMARY KEY,
    name       TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS queue_entries (
    queue_entry_id  SERIAL PRIMARY KEY,
    visit_id          INTEGER NOT NULL REFERENCES visits(visit_id),
    from_room_id       INTEGER REFERENCES rooms(room_id),
    to_room_id          INTEGER NOT NULL REFERENCES rooms(room_id),
    queued_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    called_at             TIMESTAMPTZ,
    completed_at           TIMESTAMPTZ,
    created_by              INTEGER REFERENCES system_users(system_user_id)
);

CREATE INDEX IF NOT EXISTS idx_queue_entries_visit_id ON queue_entries (visit_id);
CREATE INDEX IF NOT EXISTS idx_queue_entries_to_room_id ON queue_entries (to_room_id);
CREATE INDEX IF NOT EXISTS idx_queue_entries_active ON queue_entries (to_room_id) WHERE completed_at IS NULL;

-- A reasonable starting set of rooms — edit/add more via /queue/rooms.
INSERT INTO rooms (name) VALUES
    ('Reception'), ('Triage'), ('Consultation'), ('Lab'), ('Pharmacy'), ('Billing')
ON CONFLICT (name) DO NOTHING;

COMMIT;

DROP TABLE IF EXISTS entry;

DROP TRIGGER IF EXISTS entry_update_timestamp;

DROP TRIGGER IF EXISTS entry_insert;

DROP TRIGGER IF EXISTS entry_update;

DROP TRIGGER IF EXISTS entry_delete;

CREATE TABLE entry (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    api_key TEXT NOT NULL, 
    url TEXT NOT NULL,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(id),
    CHECK(version <> ''),
    CHECK(api_key <> ''),
    CHECK(url <> '')
)

CREATE TRIGGER entry_insert
AFTER
INSERT
    ON entry FOR EACH ROW BEGIN
VALUES
    (
        'entry',
        NEW.id,
        json_object(
            'version', NEW.version,
            'api_key', NEW.api_key,
            'url', NEW.url
        ),
        'INSERT'
    );

END;

--- Trigger on Entry Update
CREATE TRIGGER entry_update
AFTER
UPDATE
    ON entry FOR EACH ROW BEGIN
VALUES
    (
        'entry',
        NEW.id,
        json_object(
            'version', NEW.version,
            'api_key', NEW.api_key,
            'url', NEW.url
        ),
        'UPDATE'
    );

UPDATE
    entry
SET
    updated_at = CURRENT_TIMESTAMP
WHERE
    id = OLD.id;

END;

--- Trigger on Entry Delete
CREATE TRIGGER entry_delete
AFTER
    DELETE ON entry FOR EACH ROW 
    BEGIN
VALUES
    (
        'entry',
        OLD.id,
        json_object(
            'version', OLD.version,
            'api_key', OLD.api_key,
            'url', OLD.url
        ),
        'DELETE'
    );

END;
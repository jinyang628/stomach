DROP TABLE IF EXISTS inference;

DROP TRIGGER IF EXISTS inference_update_timestamp;

DROP TRIGGER IF EXISTS inference_insert;

DROP TRIGGER IF EXISTS inference_update;

DROP TRIGGER IF EXISTS inference_delete;

CREATE TABLE inference (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    entry_id TEXT NOT NULL,
    conversation TEXT NOT NULL,
    result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(version, entry_id, conversation, result),
    CHECK(version <> ''),
    CHECK(entry_id <> ''),
    CHECK(conversation <> ''),
    CHECK(result <> '')
);

CREATE TRIGGER inference_insert 
AFTER
INSERT
    ON inference FOR EACH ROW BEGIN 
VALUES
    (
        'inference', NEW.id,
        json_object(
            'version', NEW.version,
            'entry_id', NEW.entry_id,
            'conversation', NEW.conversation,
            'result', NEW.result
        ),
        'INSERT'
    );

END;

--- Trigger on Inference Update
CREATE TRIGGER inference_update
AFTER
UPDATE
    ON inference FOR EACH ROW BEGIN
VALUES 
    (
        'inference', NEW.id,
        json_object(
            'version', NEW.version,
            'entry_id', NEW.entry_id,
            'conversation', NEW.conversation,
            'result', NEW.result
        ),
        'UPDATE'
    );

UPDATE
    inference
SET 
    updated_at = CURRENT_TIMESTAMP
WHERE
    id = OLD.id;

END;

--- Trigger on Inference Delete
CREATE TRIGGER inference_delete
AFTER
    DELETE ON inference FOR EACH ROW BEGIN
VALUES
    (
        'inference', OLD.id,
        json_object(
            'version', OLD.version,
            'entry_id', OLD.entry_id,
            'conversation', OLD.conversation,
            'result', OLD.result
        ),
        'DELETE'
    );

END;
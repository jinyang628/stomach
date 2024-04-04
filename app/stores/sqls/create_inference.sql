DROP TABLE IF EXISTS inference;

DROP TRIGGER IF EXISTS inference_update_timestamp;

DROP TRIGGER IF EXISTS inference_insert;

DROP TRIGGER IF EXISTS inference_update;

DROP TRIGGER IF EXISTS inference_delete;

CREATE TABLE inference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version INTEGER NOT NULL,
    entry_id TEXT NOT NULL,
    conversation TEXT NOT NULL,
    summary TEXT,
    question TEXT,
    answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(version, entry_id, conversation, summary, question, answer),
    CHECK(version <> ''),
    CHECK(entry_id <> ''),
    CHECK(conversation <> '')
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
            'summary', NEW.summary,
            'question', NEW.question,
            'answer', NEW.answer
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
            'summary', NEW.summary,
            'question', NEW.question,
            'answer', NEW.answer
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
            'summary', OLD.summary,
            'question', OLD.question,
            'answer', OLD.answer
        ),
        'DELETE'
    );

END;
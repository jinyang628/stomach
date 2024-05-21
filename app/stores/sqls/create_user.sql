DROP TABLE IF EXISTS user;

DROP TRIGGER IF EXISTS user_update_timestamp;

DROP TRIGGER IF EXISTS user_insert;

DROP TRIGGER IF EXISTS user_update;

DROP TRIGGER IF EXISTS user_delete; 

CREATE TABLE user (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    api_key TEXT NOT NULL,
    usage INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(version, name, email, api_key),
    CHECK(version <> ''),
    CHECK(name <> ''),
    CHECK(email <> ''),
    CHECK(api_key <> '')
);


CREATE TRIGGER user_insert
AFTER
INSERT
    ON user FOR EACH ROW BEGIN
VALUES
    (
        'user',
        NEW.id,
        json_object(
            'version', NEW.version,
            'name', NEW.name,
            'email', NEW.email,
            'api_key', NEW.api_key,
            'usage', NEW.usage
        ),
        'INSERT'
    );

END;

--- Trigger on User Update
CREATE TRIGGER user_update  
AFTER
UPDATE
    ON user FOR EACH ROW BEGIN
VALUES
    (
        'user',
        NEW.id,
        json_object(
            'version', NEW.version,
            'name', NEW.name,
            'email', NEW.email,
            'api_key', NEW.api_key,
            'usage', NEW.usage
        ),
        'UPDATE'
    );

UPDATE
    user
SET 
    updated_at = CURRENT_TIMESTAMP
WHERE 
    id = OLD.id;

END;

--- Trigger on User Delete
CREATE TRIGGER user_delete
AFTER
DELETE
    ON user FOR EACH ROW BEGIN
VALUES
    (
        'user',
        OLD.id,
        json_object(
            'version', OLD.version,
            'name', OLD.name,
            'email', OLD.email,
            'api_key', OLD.api_key,
            'usage', OLD.usage
        ),
        'DELETE'
    );

END;
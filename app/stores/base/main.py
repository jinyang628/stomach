# Use this script to do testing/one time operations on the database

from app.stores.base.object import ObjectStore
import logging

log = logging.getLogger(__name__)

def main():
    obj_store = ObjectStore("user")
    obj_store.execute(sql="""
CREATE TRIGGER user_delete
AFTER
DELETE
    ON user FOR EACH ROW BEGIN
INSERT INTO
    log (
        table_name,
        row_id,
        data,
        change_type
    )
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
    """)



if __name__ == "__main__":
    main()

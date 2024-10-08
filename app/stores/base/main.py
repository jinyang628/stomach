# Use this script to do testing/one time operations on the database

import logging

from app.stores.base.object import ObjectStore

log = logging.getLogger(__name__)


def main():
    sql = """
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
    """
    obj_store = ObjectStore(table_name="inference")
    obj_store.execute(
        sql=sql
    )


if __name__ == "__main__":
    main()

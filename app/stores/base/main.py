# Use this script to do testing/one time operations on the database

import logging

from app.models.stores.user import User
from app.stores.base.object import ObjectStore
from app.stores.user import UserObjectStore

log = logging.getLogger(__name__)


def main():
    obj_store = ObjectStore(table_name="inference")
    obj_store.execute(
        sql="""
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
            'summary_chunk', OLD.summary_chunk,
            'question', OLD.question,
            'answer', OLD.answer,
            'language', OLD.language
        ),
        'DELETE'
    );

END;
"""
    )


if __name__ == "__main__":
    main()

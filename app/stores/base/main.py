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
"""
    )


if __name__ == "__main__":
    main()

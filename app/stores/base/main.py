# Use this script to do testing/one time operations on the database

import logging

from app.models.stores.user import User
from app.stores.base.object import ObjectStore
from app.stores.user import UserObjectStore

log = logging.getLogger(__name__)


def main():
    obj_store = ObjectStore(table_name="entry")
    obj_store.execute(
        sql="""
CREATE TABLE entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version INTEGER NOT NULL,
    entry_id TEXT NOT NULL,
    api_key TEXT NOT NULL, 
    url TEXT NOT NULL,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(version, entry_id, api_key, url),
    CHECK(version <> ''),
    CHECK(entry_id <> ''),
    CHECK(api_key <> ''),
    CHECK(url <> '')
)
"""
    )


if __name__ == "__main__":
    main()

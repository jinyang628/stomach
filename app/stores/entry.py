import os
import logging
from app.stores.base.object import ObjectStore

log = logging.getLogger(__name__)


class EntryObjectStore:
    _store: ObjectStore = None
    
    def __init__(self):
        self._store = ObjectStore(
            table_name=os.environ.get("TURSO_ENTRY_TABLE_NAME"),
        )
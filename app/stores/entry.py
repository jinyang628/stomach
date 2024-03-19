import os
import logging
from typing import List
from app.models.entry import Entry
from app.stores.base.object import ObjectStore

log = logging.getLogger(__name__)


class EntryObjectStore:
    _store: ObjectStore = None
    
    def __init__(self):
        self._store = ObjectStore(
            table_name=os.environ.get("TURSO_DB_ENTRY_TABLE_NAME"),
        )
        
    def insert(
        self,
        entries: List[Entry]
    ) -> List[int]:
        return self._store.insert(objs=[entry.model_dump() for entry in entries])
    
    def get(
        self,
        ids: List[int],
    ) -> List[Entry]:
        _dicts = self._store.get(ids=ids)
        return [Entry.remote(**_dict) for _dict in _dicts]
      
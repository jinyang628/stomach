import os
import logging
from typing import Any, List
from app.models.stores.entry import Entry
from app.stores.base.object import ObjectStore

log = logging.getLogger(__name__)


class EntryObjectStore:
    _store: ObjectStore = None

    def __init__(self):
        self._store = ObjectStore(
            table_name=os.environ.get("TURSO_DB_ENTRY_TABLE_NAME"),
        )

    def get(
        self,
        ids: List[int],
    ) -> List[Entry]:
        _dicts = self._store.get(ids=ids)
        return [Entry.remote(**_dict) for _dict in _dicts]

    def update(self, entries: List[Entry]) -> bool:
        return self._store.update(objs=[entry.model_dump() for entry in entries])

    def delete(self, ids: List[int]) -> bool:
        return self._store.delete(ids=ids)
    
    def insert(
        self, 
        entries: List[Entry], 
        return_column: Any = "id"
    ) -> List[str]:
        return self._store.insert(objs=[entry.model_dump() for entry in entries], return_column=return_column)
        

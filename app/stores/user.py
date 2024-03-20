import os
import logging
from app.stores.base.object import ObjectStore
from typing import List
from app.models.stores.user import User

log = logging.getLogger(__name__)


class UserObjectStore:
    _store: ObjectStore = None

    def __init__(self):
        self._store = ObjectStore(
            table_name=os.environ.get("TURSO_DB_USER_TABLE_NAME"),
        )

    def insert(self, users: List[User]) -> List[int]:
        return self._store.insert(objs=[user.model_dump() for user in users])

    def get(
        self,
        ids: List[int],
    ) -> List[User]:
        _dicts = self._store.get(ids=ids)
        return [User.remote(**_dict) for _dict in _dicts]

    def update(self, users: List[User]) -> bool:
        return self._store.update(objs=[user.model_dump() for user in users])

    def delete(self, ids: List[int]) -> bool:
        return self._store.delete(ids=ids)

import os
import logging
from app.stores.base.object import ObjectStore
from typing import Any, List
from app.models.stores.user import User

log = logging.getLogger(__name__)


class UserObjectStore:
    _store: ObjectStore = None

    def __init__(self):
        self._store = ObjectStore(
            table_name=os.environ.get("TURSO_DB_USER_TABLE_NAME"),
        )

    def insert(
        self, 
        users: List[User], 
        return_column: Any = "id"
    ) -> List[int]:
        return self._store.insert(
            objs=[user.model_dump() for user in users],
            return_column=return_column
        )

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
    
    def validate_api_key(self, api_key: str) -> bool:
        ids: list[str] = self._store.get_values_by_matching_condition(
            column_to_match="api_key",
            matching_value=api_key,
            column_to_return="id",
        )
        if len(ids) > 1:
            raise Exception(f"Multiple users found for api_key: {api_key}")
        if len(ids) == 0:
            return False
        return True

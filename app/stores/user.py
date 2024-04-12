import logging
import os
from typing import Any, List

from app.exceptions.exception import DatabaseError
from app.models.stores.user import User
from app.stores.base.object import ObjectStore

log = logging.getLogger(__name__)

USAGE_LIMIT: int = 400_000


class UserObjectStore:
    _store: ObjectStore = None

    def __init__(self):
        self._store = ObjectStore(
            table_name=os.environ.get("TURSO_DB_USER_TABLE_NAME"),
        )

    def insert(self, users: List[User], return_column: Any = "id") -> List[int]:
        return self._store.insert(
            objs=[user.model_dump() for user in users], return_column=return_column
        )

    def get_by_ids(
        self,
        ids: List[int],
    ) -> List[User]:
        _dicts = self._store.get(ids=ids)
        return [User.remote(**_dict) for _dict in _dicts]

    def update(self, users: List[User]) -> bool:
        return self._store.update(objs=[user.model_dump() for user in users])

    def delete(self, ids: List[int]) -> bool:
        return self._store.delete(ids=ids)

    def is_within_limit(self, api_key: str) -> bool:
        usage: list[int] = self._store.get_values_by_matching_condition(
            column_to_match="api_key",
            matching_value=api_key,
            column_to_return="usage",
        )
        if len(usage) > 1:
            raise Exception(f"Multiple users found for api_key: {api_key}")
        if len(usage) == 0:
            raise Exception(f"No user found for api_key: {api_key}")
        return usage[0] < USAGE_LIMIT

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

    def increment_usage(self, api_key: str, usage_counter: int) -> bool:
        rows = self._store.get_rows_by_matching_condition(
            column_to_match="api_key", matching_value=api_key
        )
        if not rows:
            raise Exception(
                f"API call is made even though the API key is invalid: {api_key}"
            )
        try:
            user_dict = self._store.convert_row_to_dict(rows[0], User)
            user = User.remote(**user_dict)
            user.usage += usage_counter
            return self.update(users=[user])
        except Exception as e:
            log.error(f"Error updating database for usage increment: {str(e)}")
            raise DatabaseError(message=str(e)) from e

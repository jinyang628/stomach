from typing import Optional
from pydantic import BaseModel

from app.models.utils import sql_value_to_typed_value


class Entry(BaseModel):
    id: Optional[int] = None
    version: int
    entry_id: str
    api_key: str
    url: str

    def local(
        version: int,
        entry_id: str,
        api_key: str,
        url: str,
    ):
        return Entry(version=version, entry_id=entry_id, api_key=api_key, url=url)

    def remote(
        **kwargs,
    ):
        entry = Entry(
            id=sql_value_to_typed_value(dict=kwargs, key="id", type=int),
            version=sql_value_to_typed_value(dict=kwargs, key="version", type=int),
            entry_id=sql_value_to_typed_value(dict=kwargs, key="entry_id", type=str),
            api_key=sql_value_to_typed_value(dict=kwargs, key="api_key", type=str),
            url=sql_value_to_typed_value(dict=kwargs, key="url", type=str),
        )
        return entry

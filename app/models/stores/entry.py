from typing import Optional
from pydantic import BaseModel

from app.models.utils import generate_identifier, sql_value_to_typed_value

# Update this version accordingly
ENTRY_VERSION: int = 1

class Entry(BaseModel):
    id: Optional[int] = None
    version: int
    entry_id: str
    api_key: str
    url: str

    @classmethod
    def local(
        cls,
        api_key: str,
        url: str,
    ):
        
        return cls(
            version=ENTRY_VERSION, 
            entry_id=generate_identifier(cls.__name__.lower()), 
            api_key=api_key, 
            url=url
        )

    @classmethod
    def remote(
        cls,
        **kwargs,
    ):
        return cls(
            id=sql_value_to_typed_value(dict=kwargs, key="id", type=int),
            version=sql_value_to_typed_value(dict=kwargs, key="version", type=int),
            entry_id=sql_value_to_typed_value(dict=kwargs, key="entry_id", type=str),
            api_key=sql_value_to_typed_value(dict=kwargs, key="api_key", type=str),
            url=sql_value_to_typed_value(dict=kwargs, key="url", type=str),
        )
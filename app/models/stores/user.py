from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.utils import sql_value_to_typed_value

USER_VERSION: int = 1


class User(BaseModel):
    id: Optional[int] = None
    version: int
    name: str
    email: str
    api_key: str
    usage: int = 0
    created_at: datetime = None
    updated_at: datetime = None

    @classmethod
    def local(
        cls,
        name: str,
        email: str,
        api_key: str,
    ):
        return cls(
            version=USER_VERSION,
            name=name,
            email=email,
            api_key=api_key,
        )

    @classmethod
    def remote(
        cls,
        **kwargs,
    ):
        return cls(
            id=sql_value_to_typed_value(dict=kwargs, key="id", type=int),
            version=sql_value_to_typed_value(dict=kwargs, key="version", type=int),
            name=sql_value_to_typed_value(dict=kwargs, key="name", type=str),
            email=sql_value_to_typed_value(dict=kwargs, key="email", type=str),
            api_key=sql_value_to_typed_value(dict=kwargs, key="api_key", type=str),
            usage=sql_value_to_typed_value(dict=kwargs, key="usage", type=int),
            created_at=sql_value_to_typed_value(
                dict=kwargs, key="created_at", type=datetime
            ),
            updated_at=sql_value_to_typed_value(
                dict=kwargs, key="updated_at", type=datetime
            ),
        )

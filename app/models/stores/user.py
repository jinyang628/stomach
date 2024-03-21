from typing import Optional
from pydantic import BaseModel

from app.models.utils import sql_value_to_typed_value

USER_VERSION: int = 1

class User(BaseModel):
    id: Optional[int] = None
    version: int
    email: str
    api_key: str

    @classmethod
    def local(
        cls,
        email: str,
        api_key: str,
    ):
        return cls(
            version=USER_VERSION,
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
            email=sql_value_to_typed_value(dict=kwargs, key="email", type=str),
            api_key=sql_value_to_typed_value(dict=kwargs, key="api_key", type=str),
        )

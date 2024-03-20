from typing import Optional
from pydantic import BaseModel

from app.models.utils import sql_value_to_typed_value


class User(BaseModel):
    id: Optional[int] = None
    version: int
    email: str
    api_key: str
    
    def local(
        version: int,
        email: str,
        api_key: str,
    ):
        return User(
            version=version,
            email=email,
            api_key=api_key,
        )
    
    def remote(
        **kwargs,
    ):
        entry = User(
            id=sql_value_to_typed_value(dict=kwargs, key="id", type=int),
            version=sql_value_to_typed_value(dict=kwargs, key="version", type=int),
            email=sql_value_to_typed_value(dict=kwargs, key="email", type=str),
            api_key=sql_value_to_typed_value(dict=kwargs, key="api_key", type=str),
        )
        return entry


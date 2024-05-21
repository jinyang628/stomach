from datetime import datetime

from app.models.stores.base import BaseObject
from app.models.utils import sql_value_to_typed_value
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base 
from sqlalchemy.sql import func

Base = declarative_base()

USER_VERSION: int = 1

class UserORM(Base):
    __tablename__ = "user"
    
    id = Column(String, primary_key=True)
    version = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    usage = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())  # Automatically use the current timestamp of the database server upon creation
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())  # Automatically use the current timestamp of the database server upon creation and update

class User(BaseObject):
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
        return User(
            id=User.generate_id(version=USER_VERSION, name=name, email=email, api_key=api_key),
            version=USER_VERSION,
            name=name,
            email=email,
            api_key=api_key
        )

    @classmethod
    def remote(
        cls,
        **kwargs,
    ):
        return cls(
            id=sql_value_to_typed_value(dict=kwargs, key="id", type=str),
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

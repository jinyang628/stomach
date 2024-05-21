from app.models.stores.base import BaseObject
from app.models.utils import sql_value_to_typed_value
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base 
from sqlalchemy.sql import func

Base = declarative_base()

# Update this version accordingly
INFERENCE_VERSION: int = 1

class InferenceORM(Base):
    __tablename__ = "inference"
    
    id = Column(String, primary_key=True)
    version = Column(Integer, nullable=False)
    entry_id = Column(String, nullable=False)
    conversation = Column(String, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())  # Automatically use the current timestamp of the database server upon creation
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())  # Automatically use the current timestamp of the database server upon creation and update

class Inference(BaseObject):
    version: int
    entry_id: str
    conversation: str
    result: str # Json string

    @classmethod
    def local(
        cls,
        entry_id: str,
        conversation: str,
        result: str
    ):
        return Inference(
            id=Inference.generate_id(version=INFERENCE_VERSION, entry_id=entry_id, conversation=conversation, result=result),
            version=INFERENCE_VERSION,
            entry_id=entry_id,
            conversation=conversation,
            result=result
        )

    @classmethod
    def remote(
        cls,
        **kwargs,
    ):
        return cls(
            id=sql_value_to_typed_value(dict=kwargs, key="id", type=str),
            version=sql_value_to_typed_value(dict=kwargs, key="version", type=int),
            entry_id=sql_value_to_typed_value(dict=kwargs, key="entry_id", type=str),
            conversation=sql_value_to_typed_value(
                dict=kwargs, key="conversation", type=str
            ),
            result=sql_value_to_typed_value(dict=kwargs, key="result", type=str),
        )

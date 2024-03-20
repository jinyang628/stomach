from typing import Optional
from pydantic import BaseModel

from app.models.utils import sql_value_to_typed_value


class Inference(BaseModel):
    id: Optional[int] = None
    version: int
    entry_id: str
    conversation: str
    summary: Optional[str]
    exercise: Optional[str]

    def local(
        version: int,
        entry_id: str,
        conversation: str,
        summary: Optional[str],
        exercise: Optional[str],
    ):
        return Inference(
            version=version,
            entry_id=entry_id,
            conversation=conversation,
            summary=summary,
            exercise=exercise,
        )

    def remote(
        **kwargs,
    ):
        inference = Inference(
            id=sql_value_to_typed_value(dict=kwargs, key="id", type=int),
            version=sql_value_to_typed_value(dict=kwargs, key="version", type=int),
            entry_id=sql_value_to_typed_value(dict=kwargs, key="entry_id", type=str),
            conversation=sql_value_to_typed_value(
                dict=kwargs, key="conversation", type=str
            ),
            summary=sql_value_to_typed_value(dict=kwargs, key="summary", type=str),
            exercise=sql_value_to_typed_value(dict=kwargs, key="exercise", type=str),
        )
        return inference

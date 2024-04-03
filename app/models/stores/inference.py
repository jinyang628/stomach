from typing import Optional

from pydantic import BaseModel

from app.models.utils import sql_value_to_typed_value

# Update this version accordingly
INFERENCE_VERSION: int = 1


class Inference(BaseModel):
    id: Optional[int] = None
    version: int
    entry_id: str
    conversation: str
    summary: Optional[str]
    question: Optional[str]
    answer: Optional[str]

    @classmethod
    def local(
        cls,
        entry_id: str,
        conversation: str,
        summary: Optional[str],
        question: Optional[str],
        answer: Optional[str],
    ):
        return cls(
            version=INFERENCE_VERSION,
            entry_id=entry_id,
            conversation=conversation,
            summary=summary,
            question=question,
            answer=answer,
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
            conversation=sql_value_to_typed_value(
                dict=kwargs, key="conversation", type=str
            ),
            summary=sql_value_to_typed_value(dict=kwargs, key="summary", type=str),
            question=sql_value_to_typed_value(dict=kwargs, key="question", type=str),
            answer=sql_value_to_typed_value(dict=kwargs, key="answer", type=str),
        )

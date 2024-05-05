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
    summary_chunk: Optional[str]
    question: Optional[str]
    half_completed_code: Optional[str]
    fully_completed_code: Optional[str]
    language: Optional[str]

    @classmethod
    def local(
        cls,
        entry_id: str,
        conversation: str,
        summary: Optional[str],
        summary_chunk: Optional[str],
        question: Optional[str],
        half_completed_code: Optional[str],
        fully_completed_code: Optional[str],
        language: Optional[str],
    ):
        return cls(
            version=INFERENCE_VERSION,
            entry_id=entry_id,
            conversation=conversation,
            summary=summary,
            summary_chunk=summary_chunk,
            question=question,
            half_completed_code=half_completed_code,
            fully_completed_code=fully_completed_code,
            language=language,
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
            summary_chunk=sql_value_to_typed_value(
                dict=kwargs, key="summary_chunk", type=str
            ),
            question=sql_value_to_typed_value(dict=kwargs, key="question", type=str),
            half_completed_code=sql_value_to_typed_value(
                dict=kwargs, key="half_completed_code", type=str
            ),
            fully_completed_code=sql_value_to_typed_value(
                dict=kwargs, key="fully_completed_code", type=str
            ),
            language=sql_value_to_typed_value(dict=kwargs, key="language", type=str),
        )

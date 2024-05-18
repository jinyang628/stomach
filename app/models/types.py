from typing import Any, List, Optional

from pydantic import BaseModel


###
### Database types
###
class EntryDbInput(BaseModel):
    # The shape of the input data to be stored in the entry table
    api_key: str
    url: str
    tasks: List[str]

    class Config:
        extra = "forbid"


class InferenceDbInput(BaseModel):
    # The shape of the input data to be stored in the inference table
    entry_id: str
    conversation: str
    summary: Optional[str]
    summary_chunk: Optional[str]
    question: Optional[str]
    half_completed_code: Optional[str]
    fully_completed_code: Optional[str]
    language: Optional[str]


###
### API types
###
class InferenceInput(BaseModel):
    # The input of the API made to Brain
    conversation: dict[str, Any]
    tasks: List[str]

    class Config:
        extra = "forbid"


class BrainResponse(BaseModel):
    summary: Optional[list[dict[str, Any]]]
    practice: Optional[list[dict[str, str]]]
    token_sum: int

    class Config:
        extra = "forbid"

    def to_dict_for_user(self):
        """Converts important elements in the BrainResponse object to a dictionary that will be passed back to fingers for the user"""

        return {
            "summary": self.summary,
            "practice": self.practice,
        }

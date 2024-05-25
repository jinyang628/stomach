from typing import Any, Optional

from pydantic import BaseModel


###
### Database types
###
class EntryDbInput(BaseModel):
    # The shape of the input data to be stored in the entry table
    api_key: str
    url: str
    content: list[str]

    class Config:
        extra = "forbid"


class InferenceDbInput(BaseModel):
    # The shape of the input data to be stored in the inference table
    entry_id: str
    conversation: str
    result: str


###
### API types
###
class InferenceInput(BaseModel):
    # The input of the API made to Brain
    conversation: dict[str, Any]
    content: list[str]

    class Config:
        extra = "forbid"


class BrainResponse(BaseModel):
    result: Optional[list[dict[str, Any]]]
    token_sum: int

    class Config:
        extra = "forbid"

    def to_dict_for_user(self):
        """Converts important elements in the BrainResponse object to a dictionary that will be passed back to fingers for the user"""

        return {
            "result": self.result,
        }

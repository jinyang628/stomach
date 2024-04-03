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
    question: Optional[str]
    answer: Optional[str]


###
### API types
###
class InferenceInput(BaseModel):
    # The input of the API made to Brain
    conversation: dict[str, Any]
    tasks: List[str]

    class Config:
        extra = "forbid"


# class BrainResponse(BaseModel):
#     summary: Optional[str]
#     code: Optional[str]

#     class Config:
#         extra = 'forbid'

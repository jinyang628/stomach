from typing import Any, List, Optional
from pydantic import BaseModel

from app.models.enum.task import Task
from app.models.logic.conversation import Conversation

class _PostEntriesInput(BaseModel):
    api_key: str
    url: str
    tasks: List[str]
    
    class Config:
        extra = 'forbid'
        
class InferenceInput(BaseModel):
    conversation: dict[str, Any]
    tasks: List[str]
    
    class Config:
        extra = 'forbid'
    
class BrainResponse(BaseModel):
    summary: Optional[str]
    code: Optional[str]
    
    class Config:
        extra = 'forbid'
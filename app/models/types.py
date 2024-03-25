from typing import Any, List, Optional
from pydantic import BaseModel

###
### Database types
### 
class EntryDbInput(BaseModel):
    api_key: str
    url: str
    tasks: List[str]
    
    class Config:
        extra = 'forbid'
        
class InferenceDbInput(BaseModel):
    entry_id: str
    conversation: str
    summary: Optional[str]
    practice: Optional[str]
    
###
### API types
###    
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
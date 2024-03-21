from typing import List
from pydantic import BaseModel

from app.models.enum.task import Task

class _PostEntriesInput(BaseModel):
    api_key: str
    url: str
    tasks: List[Task]
    
class ValidateInput(BaseModel):
    api_key: str
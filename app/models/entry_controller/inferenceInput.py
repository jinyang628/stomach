from typing import Any
from pydantic import BaseModel, ConfigDict

from app.models.entry_controller.task import Task


class InferenceInput(BaseModel):
    # This forbids extra parameters from being added into this interface
    model_config = ConfigDict(extra="forbid")
    
    entry: dict[str, Any]
    tasks: list[Task]
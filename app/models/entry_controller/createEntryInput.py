from pydantic import BaseModel, ConfigDict

from app.models.entry_controller.task import Task


class CreateEntryInput(BaseModel):
    # This forbids extra parameters from being added into this interface
    model_config = ConfigDict(extra="forbid")

    apiKey: str
    url: str
    tasks: list[Task]
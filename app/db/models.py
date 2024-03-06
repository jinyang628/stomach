import uuid
from pydantic import BaseModel, Field

class Entry(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    messages: dict

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "messages": {
                    "human": "Hello, World!",
                    "AI": "Goodbye, World!"
                }

            }
        }
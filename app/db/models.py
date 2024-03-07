import uuid
import re
from typing import Dict
from pydantic import BaseModel, Field, root_validator

class Entry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    messages: Dict[str, str]

    @classmethod
    @root_validator(pre=True)  # pre=True to allow the validator to run before any other validation
    def check_messages_keys(cls, values):
        messages = values.get('messages', {})
        pattern = re.compile(r"^(Assistant|User)\d+$")

        for key in messages.keys():
            if not pattern.match(key):
                raise ValueError(f"Key '{key}' does not match 'Assistant{{INTEGER}}' or 'User{{INTEGER}}' pattern")
        
        return values

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "messages": {
                    "User1": "Hello, World!",
                    "Assistant1": "Goodbye, World!"
                }
            }
        }

import re
from typing import Dict
from pydantic import BaseModel, root_validator


class BaseEntry(BaseModel):
    user_id: str
    messages: Dict[str, str]

    @root_validator(pre=True)
    def check_messages_keys(cls, values):
        messages = values.get("messages", {})
        keys = list(messages.keys())

        if not keys or keys[0] != "title":
            raise ValueError("The first key must be 'title'.")

        pattern = re.compile(r"^(AssistantMessage|UserMessage)\d+$")

        for key in keys[1:]:
            if not pattern.match(key):
                raise ValueError(
                    f"Key '{key}' does not match 'Assistant{{INTEGER}}' or 'User{{INTEGER}}' pattern"
                )

        return values

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "123456789",
                "messages": {
                    "title": "User Request Summarized",
                    "UserMessage1": "hi",
                    "AssistantMessage1": "Hello! How can I assist you today?",
                    "UserMessage2": "test",
                    "AssistantMessage2": "Sure, feel free to ask any question or tell me what you'd like to do!",
                },
            }
        }


class Entry(BaseEntry):
    pass

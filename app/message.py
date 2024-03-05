from abc import ABC
from typing import Optional


class Message(ABC):
    prev_message: Optional["Message"]
    next_message: Optional["Message"]

class UserMessage(Message):
    content: str
    
class AssistantMessage(Message):
    content: str
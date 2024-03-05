from abc import ABC
from typing import Optional


class Message(ABC):
    content: str
    prev_message: Optional["Message"]
    next_message: Optional["Message"]
    
    def __init__(self, content: str, prev_message: Optional["Message"], next_message: Optional["Message"]):
        if not isinstance(content, str):
            raise TypeError("Content must be a string")
        self.content = content
        self.prev_message = prev_message
        self.next_message = next_message

class UserMessage(Message):    
    pass
    
class AssistantMessage(Message):    
    pass
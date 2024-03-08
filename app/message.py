from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Message(ABC):
    _content: str

    def __init__(self, content: str):
        if not isinstance(content, str):
            raise TypeError("Content must be a string")
        self._content = content

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Content must be a string")
        self._content = value
        
    def __str__(self):
        return self._content


@dataclass
class UserMessage(Message):
    
    _id: int    
    _prev_message: Optional["AssistantMessage"]
    _next_message: Optional["AssistantMessage"]
    
    instance_count: int = 0
    
    def __init__(
        self,
        content: str,
        prev_message: Optional["AssistantMessage"],
        next_message: Optional["AssistantMessage"],
    ):
        super().__init__(content)
        if not isinstance(prev_message, (AssistantMessage, type(None))):
            raise TypeError("Previous message must be an AssistantMessage or None")
        self._prev_message = prev_message
        if not isinstance(next_message, (AssistantMessage, type(None))):
            raise TypeError("Next message must be an AssistantMessage or None")
        self._next_message = next_message
        UserMessage.instance_count += 1
        self._id = UserMessage.instance_count

    @property
    def prev_message(self) -> Optional["AssistantMessage"]:
        return self._prev_message

    @prev_message.setter
    def prev_message(self, value: Optional["AssistantMessage"]):
        if not isinstance(value, (AssistantMessage, type(None))):
            raise TypeError("Previous message must be an AssistantMessage or None")
        self._prev_message = value

    @property
    def next_message(self) -> Optional["AssistantMessage"]:
        return self._next_message

    @next_message.setter
    def next_message(self, value: Optional["AssistantMessage"]):
        if not isinstance(value, (AssistantMessage, type(None))):
            raise TypeError("Next message must be an AssistantMessage or None")
        self._next_message = value
        
    @property
    def id(self) -> int:
        return self._id

@dataclass
class AssistantMessage(Message):

    _id: int    
    _prev_message: Optional["UserMessage"]
    _next_message: Optional["UserMessage"]
    
    instance_count: int = 0

    def __init__(
        self,
        content: str,
        prev_message: Optional["UserMessage"],
        next_message: Optional["UserMessage"],
    ):
        super().__init__(content)
        if not isinstance(prev_message, (UserMessage, type(None))):
            raise TypeError("Previous message must be a UserMessage or None")
        self._prev_message = prev_message
        if not isinstance(next_message, (UserMessage, type(None))):
            raise TypeError("Next message must be a UserMessage or None")
        self._next_message = next_message
        AssistantMessage.instance_count += 1
        self._id = AssistantMessage.instance_count

    @property
    def prev_message(self) -> Optional["UserMessage"]:
        return self._prev_message

    @prev_message.setter
    def prev_message(self, value: Optional["UserMessage"]):
        if not isinstance(value, (UserMessage, type(None))):
            raise TypeError("Previous message must be a UserMessage or None")
        self._prev_message = value

    @property
    def next_message(self) -> Optional["UserMessage"]:
        return self._next_message

    @next_message.setter
    def next_message(self, value: Optional["UserMessage"]):
        if not isinstance(value, (UserMessage, type(None))):
            raise TypeError("Next message must be a UserMessage or None")
        self._next_message = value
        
    @property
    def id(self) -> int:
        return self._id

        
    
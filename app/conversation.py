from app.message import Message


class Conversation:
    _title: str
    _curr_message: Message

    def __init__(self, title: str, curr_message: Message):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        self._title = title
        if not isinstance(curr_message, Message):
            raise TypeError("Current message must be a Message instance")
        self._curr_message = curr_message

    @property
    def title(self) -> str:
        return self._title

    @property
    def curr_message(self) -> Message:
        return self._curr_message

    @curr_message.setter
    def curr_message(self, value: Message):
        if not isinstance(value, Message):
            raise TypeError("Current message must be a Message instance")
        self._curr_message = value

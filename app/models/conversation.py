from app.models.message import Message


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

    # We are using static variables to instantiate the counters in each Message class so this function is very difficult to test. Do NOT make unnecessary modifications.
    def jsonify(self) -> dict[str, str]:
        result: dict[str, str] = {"title": self._title}

        # Start with the current message
        current: Message = self._curr_message
        messages: list[Message] = []

        # Traverse backwards
        while current:
            messages.insert(0, current)
            current = current.prev_message if hasattr(current, "prev_message") else None

        # Reset to current message and traverse forwards
        current = (
            self._curr_message.next_message
            if hasattr(self._curr_message, "next_message")
            else None
        )
        while current:
            messages.append(current)
            current = current.next_message if hasattr(current, "next_message") else None

        # Add messages to result
        for message in messages:
            key = f"{type(message).__name__}{message.id}"
            result[key] = str(message)

        return result

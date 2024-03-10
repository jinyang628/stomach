import pytest
from app.models.message import UserMessage, AssistantMessage
from app.models.conversation import Conversation

CONVERSATION_TEST_DATA = [
    ("Valid Title", UserMessage("Valid Message", None, None), None),
    (123, AssistantMessage("Valid Message", None, None), TypeError),
    ("Valid Title", "Invalid Message", TypeError),
]


@pytest.mark.parametrize(
    "title, curr_message, expected_exception", CONVERSATION_TEST_DATA
)
def test_conversation_init(title, curr_message, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            Conversation(title, curr_message)
    else:
        conversation = Conversation(title, curr_message)
        assert conversation.title == title
        assert conversation.curr_message == curr_message

import pytest
from app.message import UserMessage, AssistantMessage

@pytest.fixture
def assistant_message_fixture():
    return AssistantMessage(content="Assistant", prev_message=None, next_message=None)

@pytest.fixture
def user_message_fixture():
    return UserMessage(content="User", prev_message=None, next_message=None)

def test_assistant_message_valid(user_message_fixture):
    assistant_message_1 = AssistantMessage(content="Assistant", prev_message=None, next_message=None)
    assert assistant_message_1.content == "Assistant"
    assert assistant_message_1.prev_message is None
    assert assistant_message_1.next_message is None

    assistant_message_2 = AssistantMessage(content="Assistant", prev_message=user_message_fixture, next_message=None)
    assert assistant_message_2.content == "Assistant"
    assert assistant_message_2.prev_message == user_message_fixture
    assert assistant_message_2.next_message is None

    assistant_message_3 = AssistantMessage(content="Assistant", prev_message=None, next_message=user_message_fixture)
    assert assistant_message_3.content == "Assistant"
    assert assistant_message_3.prev_message is None
    assert assistant_message_3.next_message == user_message_fixture

    assistant_message_4 = AssistantMessage(content="Assistant", prev_message=user_message_fixture, next_message=user_message_fixture)
    assert assistant_message_4.content == "Assistant"
    assert assistant_message_4.prev_message == user_message_fixture
    assert assistant_message_4.next_message == user_message_fixture
    
def test_user_message_valid(assistant_message_fixture):
    user_message_1 = UserMessage(content="User", prev_message=None, next_message=None)
    assert user_message_1.content == "User"
    assert user_message_1.prev_message is None
    assert user_message_1.next_message is None

    user_message_2 = UserMessage(content="User", prev_message=assistant_message_fixture, next_message=None)
    assert user_message_2.content == "User"
    assert user_message_2.prev_message == assistant_message_fixture
    assert user_message_2.next_message is None

    user_message_3 = UserMessage(content="User", prev_message=None, next_message=assistant_message_fixture)
    assert user_message_3.content == "User"
    assert user_message_3.prev_message is None
    assert user_message_3.next_message == assistant_message_fixture

    user_message_4 = UserMessage(content="User", prev_message=assistant_message_fixture, next_message=assistant_message_fixture)
    assert user_message_4.content == "User"
    assert user_message_4.prev_message == assistant_message_fixture
    assert user_message_4.next_message == assistant_message_fixture

MESSAGE_INVALID_DATA = [
    (None, None, None, TypeError),
    (123, "prev_message_instance", "next_message_instance", TypeError),
    ("Message", 551, "next_message_instance", TypeError),
    ("Message", "prev_message_instance", 220, TypeError), 
]

@pytest.mark.parametrize("content, prev_message, next_message, expected_exception", MESSAGE_INVALID_DATA)
def test_message_invalid(content, prev_message, next_message, expected_exception):
    with pytest.raises(expected_exception):
        user_message = UserMessage(content, prev_message, next_message)
    
    with pytest.raises(expected_exception):
        assistant_message = AssistantMessage(content, prev_message, next_message)

SETTER_TEST_DATA = [
    (UserMessage, "prev_message", AssistantMessage("Valid AssistantMessage", None, None), None),
    (UserMessage, "next_message", AssistantMessage("Valid AssistantMessage", None, None), None),
    (UserMessage, "prev_message", UserMessage("Valid AssistantMessage", None, None), TypeError),
    (UserMessage, "next_message", UserMessage("Valid AssistantMessage", None, None), TypeError),
    (AssistantMessage, "prev_message", UserMessage("Valid UserMessage", None, None), None),
    (AssistantMessage, "next_message", UserMessage("Valid UserMessage", None, None), None),
    (AssistantMessage, "prev_message", AssistantMessage("Valid UserMessage", None, None), TypeError),
    (AssistantMessage, "next_message", AssistantMessage("Valid UserMessage", None, None), TypeError),
]

@pytest.mark.parametrize("message_class, setter_attr, value, expected_exception", SETTER_TEST_DATA)
def test_message_setters(message_class, setter_attr, value, expected_exception):
    message = message_class("Initial content", None, None)
    
    if expected_exception:
        with pytest.raises(expected_exception):
            setattr(message, setter_attr, value)
    else:
        setattr(message, setter_attr, value)
        assert getattr(message, setter_attr) == value
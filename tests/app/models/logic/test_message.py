import copy

import pytest

from app.models.logic.message import AssistantMessage, UserMessage

###
### USER MESSAGE TESTS
###
VALID_USER_MESSAGE_INITIALISATION_DATA = [
    (
        "I love test cases!",
        None,
        None,
    ),
    (
        "tests/app/stores/test_entry.py.tests/app/stores/test_inference.66%",
        AssistantMessage(
            content="prev",
            prev_message=UserMessage(
                content="dummy1", prev_message=None, next_message=None
            ),
            next_message=None,
        ),
        AssistantMessage(
            content="next",
            prev_message=UserMessage(
                content="dummy2", prev_message=None, next_message=None
            ),
            next_message=None,
        ),
    ),
    (
        "tests/app/stores/test_entry.py.tests/app/stores/test_inference.66%",
        None,
        AssistantMessage(
            content="next",
            prev_message=UserMessage(
                content="dummy", prev_message=None, next_message=None
            ),
            next_message=None,
        ),
    ),
]


@pytest.mark.parametrize(
    "content, prev_message, next_message", VALID_USER_MESSAGE_INITIALISATION_DATA
)
def test_valid_user_message_initialisation(content, prev_message, next_message):
    user_message = UserMessage(
        content=content, prev_message=prev_message, next_message=next_message
    )
    assert user_message.content == content
    assert user_message.prev_message == prev_message
    assert user_message.next_message == next_message


INVALID_USER_MESSAGE_INITIALISATION_DATA = [
    (
        123,
        None,
        None,
    ),
    (
        "tests/app/stores/test_entry.py.tests/app/stores/test_inference.66%",
        UserMessage(content="prev", prev_message=None, next_message=None),
        UserMessage(content="next", prev_message=None, next_message=None),
    ),
    (
        "tests/app/stores/test_entry.py.tests/app/stores/test_inference.66%",
        None,
        UserMessage(content="next", prev_message=None, next_message=None),
    ),
]


@pytest.mark.parametrize(
    "content, prev_message, next_message", INVALID_USER_MESSAGE_INITIALISATION_DATA
)
def test_invalid_user_message_initialisation(content, prev_message, next_message):
    with pytest.raises(TypeError):
        UserMessage(
            content=content, prev_message=prev_message, next_message=next_message
        )


@pytest.mark.parametrize(
    "content, prev_message, next_message", VALID_USER_MESSAGE_INITIALISATION_DATA
)
def test_valid_prev_next_user_message_reference_and_set(
    content, prev_message, next_message
):
    user_message = UserMessage(
        content=content, prev_message=prev_message, next_message=next_message
    )
    assert user_message.prev_message == prev_message
    assert user_message.next_message == next_message
    prev_message_copy = copy.copy(user_message.prev_message)
    user_message.prev_message = user_message.next_message
    user_message.next_message = prev_message_copy
    assert user_message.prev_message == next_message
    assert user_message.next_message == prev_message


INVALID_USER_MESSAGE_SET_DATA = [
    (
        UserMessage(content="prev", prev_message=None, next_message=None),
        UserMessage(content="next", prev_message=None, next_message=None),
    ),
    (
        123,
        {"content": "next", "prev_message": None, "next_message": None},
    ),
]


@pytest.mark.parametrize("prev_message, next_message", INVALID_USER_MESSAGE_SET_DATA)
def test_invalid_user_prev_next_message_set(prev_message, next_message):
    user_message = UserMessage(
        content="I love test cases!", prev_message=None, next_message=None
    )
    with pytest.raises(TypeError):
        user_message.prev_message = prev_message
    with pytest.raises(TypeError):
        user_message.next_message = next_message


###
### ASSISTANT MESSAGE TESTS
###
VALID_ASSISTANT_MESSAGE_INITIALISATION_DATA = [
    (
        "tests/app/stores/test_entry.py.tests/app/stores/test_inference.66%",
        UserMessage(content="prev", prev_message=None, next_message=None),
        UserMessage(content="next", prev_message=None, next_message=None),
    ),
    (
        "tests/app/stores/test_entry.py.tests/app/stores/test_inference.66%",
        UserMessage(content="next", prev_message=None, next_message=None),
        None,
    ),
]


@pytest.mark.parametrize(
    "content, prev_message, next_message", VALID_ASSISTANT_MESSAGE_INITIALISATION_DATA
)
def test_valid_asssitant_message_initialisation(content, prev_message, next_message):
    assistant_message = AssistantMessage(
        content=content, prev_message=prev_message, next_message=next_message
    )
    assert assistant_message.content == content
    assert assistant_message.prev_message == prev_message
    assert assistant_message.next_message == next_message


INVALID_ASSISTANT_MESSAGE_INITIALISATION_DATA = [
    (
        123,
        None,
        None,
    ),
    (
        "tests/app/stores/test_entry.py.tests/app/stores/test_inference.66%",
        AssistantMessage(
            content="prev",
            prev_message=UserMessage(
                content="dummy1", prev_message=None, next_message=None
            ),
            next_message=None,
        ),
        AssistantMessage(
            content="next",
            prev_message=UserMessage(
                content="dummy2", prev_message=None, next_message=None
            ),
            next_message=None,
        ),
    ),
    (
        "tests/app/stores/test_entry.py.tests/app/stores/test_inference.66%",
        None,
        AssistantMessage(
            content="next",
            prev_message=UserMessage(
                content="dummy", prev_message=None, next_message=None
            ),
            next_message=None,
        ),
    ),
]


@pytest.mark.parametrize(
    "content, prev_message, next_message", INVALID_ASSISTANT_MESSAGE_INITIALISATION_DATA
)
def test_invalid_assistant_message_initialisation(content, prev_message, next_message):
    with pytest.raises(TypeError):
        AssistantMessage(
            content=content, prev_message=prev_message, next_message=next_message
        )


@pytest.mark.parametrize(
    "content, prev_message, next_message", VALID_ASSISTANT_MESSAGE_INITIALISATION_DATA
)
def test_valid_prev_next_assistant_message_reference_and_set(
    content, prev_message, next_message
):
    assistant_message = AssistantMessage(
        content=content, prev_message=prev_message, next_message=next_message
    )
    assert assistant_message.prev_message == prev_message
    assert assistant_message.next_message == next_message
    prev_message_copy = copy.copy(assistant_message.prev_message)
    assistant_message.prev_message = assistant_message.next_message
    assistant_message.next_message = prev_message_copy
    assert assistant_message.prev_message == next_message
    assert assistant_message.next_message == prev_message


INVALID_ASSISTANT_MESSAGE_SET_DATA = [
    (
        AssistantMessage(
            content="prev",
            prev_message=UserMessage(
                content="dummy1", prev_message=None, next_message=None
            ),
            next_message=None,
        ),
        AssistantMessage(
            content="next",
            prev_message=UserMessage(
                content="dummy2", prev_message=None, next_message=None
            ),
            next_message=None,
        ),
    ),
    (
        123,
        {"content": "next", "prev_message": None, "next_message": None},
    ),
]


@pytest.mark.parametrize(
    "prev_message, next_message", INVALID_ASSISTANT_MESSAGE_SET_DATA
)
def test_invalid_prev_next_assistant_message_set(prev_message, next_message):
    assistant_message = AssistantMessage(
        content="I love test cases!",
        prev_message=UserMessage(content="dummy", prev_message=None, next_message=None),
        next_message=None,
    )
    with pytest.raises(TypeError):
        assistant_message.prev_message = prev_message
    with pytest.raises(TypeError):
        assistant_message.next_message = next_message

import pytest
from app.models.logic.message import UserMessage, AssistantMessage
from app.models.logic.conversation import Conversation 

VALID_CONVERSATION_INITIALISATION_DATA = [
    (
        "I love test cases!",
        UserMessage(content="First message", prev_message=None, next_message=None),
    )
]

@pytest.mark.parametrize("title, message", VALID_CONVERSATION_INITIALISATION_DATA)
def test_jsonify_message(title, message, expected_output):
    conversation = Conversation(title=title, curr_message=message)
    assert conversation.curr_message == message    



msg1 = UserMessage(content="First message", prev_message=None, next_message=None)
msg2 = AssistantMessage(content="Second message", prev_message=msg1, next_message=None)
msg1.next_message = msg2
msg3 = UserMessage(content="Third message", prev_message=msg2, next_message=None)
msg2.next_message = msg3

JSONIFY_MESSAGE_DATA = [
    (
        "Single Message Test", 
        UserMessage(content="Single message", prev_message=None, next_message=None), 
        {
            "title": "Single Message Test",
            "UserMessage1": "Single message"
        }
    ),
     (
        "Multiple Messages Test", 
        msg3, 
        {
            "title": "Multiple Messages Test",
            "UserMessage1": "First message",
            "AssistantMessage1": "Second message",
            "UserMessage2": "Third message"
        }
    )
]

@pytest.mark.parametrize("title, message, expected_output", JSONIFY_MESSAGE_DATA)
def test_jsonify_message(title, message, expected_output):
    conversation = Conversation(title=title, curr_message=message)
    assert conversation.jsonify() == expected_output    

# import pytest
# from app.message import UserMessage, AssistantMessage

# from pydantic import ValidationError

# MESSAGE_VALID_DATA = [
#     ("Hello, User!", None, None),
#     ("User message", UserMessage("prev_message_instance"), AssistantMessage("next_message_instance")),
#     ("User message", None, "next_message_instance")
# ]

# @pytest.mark.parametrize("content, prev_message, next_message", MESSAGE_VALID_DATA)
# def test_message_valid(content, prev_message, next_message):
#     user_message = UserMessage(content, prev_message, next_message)
#     assert user_message.content == content
#     assert user_message.prev_message == prev_message
#     assert user_message.next_message == next_message
    
#     assistant_message = AssistantMessage(content, prev_message, next_message)
#     assert assistant_message.content == content
#     assert assistant_message.prev_message == prev_message
#     assert assistant_message.next_message == next_message

# MESSAGE_INVALID_DATA = [
#     (None, None, None),
#     (123, "prev_message_instance", "next_message_instance"),
#     ("User message", 551, "next_message_instance"),
#     ("User message", "prev_message_instance", 220)
# ]

# @pytest.mark.parametrize("content, prev_message, next_message", MESSAGE_INVALID_DATA)
# def test_message_invalid(content, prev_message, next_message):
#     user_message = UserMessage(content, prev_message, next_message)
    
#     assistant_message = AssistantMessage(content, prev_message, next_message)

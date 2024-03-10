import pytest
from app.models.entry import Entry

def test_entry_valid_data():
    """Test the Entry model with valid data."""
    valid_data = {
        "user_id": "some_user_id",
        "messages": {
            "title": "User Request Summarized",
            "UserMessage1": "hi",
            "AssistantMessage1": "Hello! How can I assist you today?",
            "UserMessage2": "test",
            "AssistantMessage2": "Sure, feel free to ask any question or tell me what you'd like to do!"
        }
    }
    entry = Entry(**valid_data)
    assert entry.user_id == "some_user_id"
    assert "title" in entry.messages
    assert entry.messages["title"] == "User Request Summarized"

def test_entry_missing_title():
    """Test the Entry model with missing 'title' key."""
    invalid_data_missing_title = {
        "user_id": "some_user_id",
        "messages": {
            "UserMessage1": "hi",
            "AssistantMessage1": "Hello! How can I assist you today?",
        }
    }
    with pytest.raises(ValueError) as e:
        Entry(**invalid_data_missing_title)
    assert "The first key must be 'title'." in str(e.value)

def test_entry_invalid_key_pattern():
    """Test the Entry model with invalid key pattern in messages."""
    invalid_data_key_pattern = {
        "user_id": "some_user_id",
        "messages": {
            "title": "Incorrect Pattern",
            "InvalidKey": "This should fail",
        }
    }
    with pytest.raises(ValueError) as e:
        Entry(**invalid_data_key_pattern)
    assert "does not match 'Assistant{INTEGER}' or 'User{INTEGER}' pattern" in str(e.value)


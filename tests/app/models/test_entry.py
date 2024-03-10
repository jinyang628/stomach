import pytest
from pydantic import ValidationError
from app.models.entry import BaseEntry

def test_base_entry_valid_data():
    """Test BaseEntry with valid data."""
    entry_data = {
        "user_id": "test_user_id",
        "messages": {
            "title": "Test Title",
            "UserMessage1": "This is a test message from the user.",
            "AssistantMessage1": "This is a test response from the assistant."
        }
    }
    entry = BaseEntry(**entry_data)
    assert entry.user_id == "test_user_id"
    assert entry.messages["title"] == "Test Title"
    assert "UserMessage1" in entry.messages
    assert "AssistantMessage1" in entry.messages

def test_base_entry_invalid_no_title():
    """Test BaseEntry raises an error if the first key is not 'title'."""
    entry_data = {
        "user_id": "test_user_id",
        "messages": {
            "UserMessage1": "This is a test message from the user.",
            "AssistantMessage1": "This is a test response from the assistant."
        }
    }
    with pytest.raises(ValidationError) as excinfo:
        BaseEntry(**entry_data)
    assert "The first key must be 'title'." in str(excinfo.value)

def test_base_entry_invalid_key_pattern():
    """Test BaseEntry raises an error for keys that don't match the expected pattern."""
    entry_data = {
        "user_id": "test_user_id",
        "messages": {
            "title": "Test Title",
            "InvalidKey": "This should fail.",
        }
    }
    with pytest.raises(ValidationError) as excinfo:
        BaseEntry(**entry_data)
    assert "does not match 'Assistant{INTEGER}' or 'User{INTEGER}' pattern" in str(excinfo.value)


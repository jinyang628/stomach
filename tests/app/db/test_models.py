import uuid
from app.db.models import Entry

def test_entry_model_instantiation():
    """Test if the Entry model can be instantiated correctly."""
    entry_data = {
        "messages": {
            "human": "Why is the sky blue?",
            "AI": "The sky is blue due to the scattering of sunlight by the earth's atmosphere."
        }
    }
    entry = Entry(**entry_data)

    # Test if 'id' is generated and is a valid UUID
    assert isinstance(entry.id, str)
    assert uuid.UUID(entry.id)

    # Test if 'messages' is correctly assigned
    assert entry.messages == entry_data["messages"]

def test_entry_model_example():
    """Test if the Entry model example matches the expected format."""
    example = Entry.Config.schema_extra['example']
    expected_messages = {
        "human": "Hello, World!",
        "AI": "Goodbye, World!"
    }

    # Test if example '_id' is a valid UUID
    assert uuid.UUID(example["_id"])

    # Test if example 'messages' match the expected dictionary
    assert example["messages"] == expected_messages
import pytest
from pydantic import ValidationError

from app.models.enum.task import Task
from app.models.types import BrainResponse, EntryDbInput, InferenceInput

ENTRY_DB_INPUT_VALID_DATA = [
    ("test_api_key", "https://test_url.com", [Task.SUMMARISE, Task.PRACTICE]),
]


@pytest.mark.parametrize("api_key, url, tasks", ENTRY_DB_INPUT_VALID_DATA)
def test_post_entries_input_valid_data(api_key, url, tasks):
    try:
        input_data = EntryDbInput(api_key=api_key, url=url, tasks=tasks)
        assert input_data.api_key == api_key
        assert input_data.url == url
        assert input_data.tasks == tasks
    except ValidationError:
        pytest.fail(
            "Validation error raised unexpectedly for _post_entries_input_valid_data"
        )


ENTRY_DB_INPUT_INVALID_DATA = [
    # Missing
    (None, "https://test_url.com", [Task.SUMMARISE, Task.PRACTICE]),
    ("test_api_key", None, [Task.SUMMARISE, Task.PRACTICE]),
    ("test_api_key", "https://test_url.com", None),
    # Wrong type
    (123, "https://test_url.com", [Task.SUMMARISE, Task.PRACTICE]),
    ("test_api_key", 123, "a list of tasks"),
]


@pytest.mark.parametrize("api_key, url, tasks", ENTRY_DB_INPUT_INVALID_DATA)
def test_post_entries_input_invalid_data(api_key, url, tasks):
    with pytest.raises(ValidationError):
        EntryDbInput(api_key=api_key, url=url, tasks=tasks)


INFERENCE_INPUT_VALID_DATA = [
    (
        {
            "title": "test_title",
            "UserMessage1": "First message",
            "AssistantMessage1": "Second message",
        },
        [Task.SUMMARISE],
    ),
    (
        {
            "title": "test_title",
            "UserMessage1": "First message",
            "AssistantMessage1": "Second message",
        },
        [Task.SUMMARISE, Task.PRACTICE],
    ),
]


@pytest.mark.parametrize("conversation, tasks", INFERENCE_INPUT_VALID_DATA)
def test_inference_input_valid_data(conversation, tasks):
    try:
        input_data = InferenceInput(conversation=conversation, tasks=tasks)
        assert input_data.conversation == conversation
        assert input_data.tasks == tasks
    except ValidationError:
        pytest.fail(
            "Validation error raised unexpectedly for _post_entries_input_valid_data"
        )


INFERENCE_INPUT_INVALID_DATA = [
    ("test_conversation", [Task.SUMMARISE, Task.PRACTICE]),
    (123, [Task.SUMMARISE]),
    (
        {
            "title": "test_title",
            "UserMessage1": "First message",
            "AssistantMessage1": "Second message",
        },
        "task_summarise",
    ),
]

@pytest.mark.parametrize("conversation, tasks", INFERENCE_INPUT_INVALID_DATA)
def test_inference_input_invalid_data(conversation, tasks):
    with pytest.raises(ValidationError):
        InferenceInput(conversation=conversation, tasks=tasks)


BRAIN_RESPONSE_VALID_DATA = [
    ({"key1": "value1"}, [{"language": "python", "question": "Q1", "answer": "A1"}], 1000),
    (None, [{"language": "python", "question": "Q1", "answer": "A1"}], 1000),
    ({"key1": "value1"}, None, 1000),
    (None, None, 1000),
]

@pytest.mark.parametrize("summary, practice, token_sum", BRAIN_RESPONSE_VALID_DATA)
def test_brain_response_valid_data(summary, practice, token_sum):
    try:
        response = BrainResponse(summary=summary, practice=practice, token_sum=token_sum)
        assert response.summary == summary
        assert response.practice == practice
        assert response.token_sum == token_sum
    except ValidationError:
        pytest.fail("Validation error raised unexpectedly for valid BrainResponse data")

BRAIN_RESPONSE_INVALID_DATA = [
    ({"key": "value"}, [{"language": "python", "question": "Q1", "answer": "A1"}], None),
    ("invalid_summary_type", [{"language": "python", "question": "Q1", "answer": "A1"}], 1000),
    ({"key": "value"}, "invalid_practice_type", 1000),
    ({"key": "value"}, [{"language": "python", "question": "Q1", "answer": "A1"}], "invalid"),
]

@pytest.mark.parametrize("summary, practice, token_sum", BRAIN_RESPONSE_INVALID_DATA)
def test_brain_response_invalid_data(summary, practice, token_sum):
    with pytest.raises(ValidationError):
        BrainResponse(summary=summary, practice=practice, token_sum=token_sum)

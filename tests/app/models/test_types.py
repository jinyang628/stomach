from pydantic import ValidationError
import pytest
from app.models.enum.task import Task
from app.models.types import _PostEntriesInput


_POST_ENTRIES_INPUT_VALID_DATA = [
    ("test_api_key", "https://test_url.com", [Task.SUMMARISE, Task.PRACTICE]),
]

@pytest.mark.parametrize("api_key, url, tasks", _POST_ENTRIES_INPUT_VALID_DATA)
def test_post_entries_input_valid_data(api_key, url, tasks):
    try:
        input_data = _PostEntriesInput(api_key=api_key, url=url, tasks=tasks)
        assert input_data.api_key == api_key
        assert input_data.url == url
        assert input_data.tasks == tasks
    except ValidationError:
        pytest.fail("Validation error raised unexpectedly for _post_entries_input_valid_data")
        
_POST_ENTRIES_INPUT_INVALID_DATA = [
    # Missing
    (None, "https://test_url.com", [Task.SUMMARISE, Task.PRACTICE]),
    ("test_api_key", None, [Task.SUMMARISE, Task.PRACTICE]),
    ("test_api_key", "https://test_url.com", None),
    
    # Wrong type
    (123, "https://test_url.com", [Task.SUMMARISE, Task.PRACTICE]),
    ("test_api_key", 123, "a list of tasks"),
]

@pytest.mark.parametrize("api_key, url, tasks", _POST_ENTRIES_INPUT_INVALID_DATA)

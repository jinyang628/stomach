import json
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import HTTPException
from httpx import Response

from app.controllers.entry_controller import EntryController
from app.models.enum.task import Task
from app.models.stores.entry import Entry
from app.models.types import BrainResponse, EntryDbInput, InferenceDbInput, InferenceInput
from app.services.entry_service import EntryService


@pytest.fixture
def mock_store():
    with patch("app.services.entry_service.EntryObjectStore") as mock:
        yield mock


@pytest.fixture
def entry_inputs():
    return [
        Entry.local(
            api_key="test_api_key1", url="http://test.url1", entry_id="test_entry_id1"
        ),
        Entry.local(
            api_key="test_api_key2", url="http://test.url2", entry_id="test_entry_id2"
        ),
    ]


# @pytest.mark.asyncio
# async def test_start_entry_process_success(mocker):
#     # Mocking external functions
#     mocker.patch('asyncio.create_task', new=AsyncMock())
#     mocker.patch('app.services.entry_service.EntryService.extract_url_content', new=AsyncMock())

#     controller = EntryController(service=EntryService())
#     input = EntryDbInput(api_key="test", url="http://example.com", tasks=[Task.SUMMARISE])
#     result = await controller.start_entry_process(input)

#     assert result is not None

# @pytest.mark.asyncio
# async def test_start_entry_process_failure(mocker):
#     mocker.patch('asyncio.create_task', new=AsyncMock())
#     mocker.patch('app.services.entry_service.EntryService.extract_url_content', new=AsyncMock(side_effect=Exception("Test Exception")))

#     controller = EntryController()
#     input = EntryDbInput(api_key="test", url="http://example.com", tasks=[Task.SUMMARISE])

#     with pytest.raises(HTTPException) as exc_info:
#         await controller.start_entry_process(input)

#     assert exc_info.value.status_code == 500
#     assert "Test Exception" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_post_success(mock_store, entry_inputs):
    expected_entry_ids = ["test_entry_id1", "test_entry_id2"]
    mock_store.return_value.insert.return_value = expected_entry_ids
    entry_ids = await EntryService().post(data=entry_inputs, return_column="entry_id")

    assert entry_ids == expected_entry_ids
    mock_store.return_value.insert.assert_called_once()
    args, kwargs = mock_store.return_value.insert.call_args
    assert "entries" in kwargs
    entries = kwargs["entries"]

    assert len(entries) == len(entry_inputs)
    for entry, input in zip(entries, entry_inputs):
        assert isinstance(entry, Entry)
        assert entry.api_key == input.api_key
        assert entry.url == input.url


@pytest.mark.asyncio
async def test_post_handles_exceptions(mock_store, entry_inputs):
    mock_store.return_value.insert.side_effect = Exception("Test Exception")

    with pytest.raises(Exception) as excinfo:
        await EntryService().post(data=entry_inputs, return_column="id")

    assert "Test Exception" in str(excinfo.value)


@pytest.fixture
def inference_input():
    return InferenceInput(
        conversation={"message": "Hello"}, tasks=[Task.SUMMARISE, Task.PRACTICE]
    )


@pytest.mark.asyncio
async def test_infer_successful(inference_input):
    mock_response_data = {
        "summary": {"key": "value"},
        "practice": [
            {
                "language": "python",
                "question": "question_code",
                "answer": "answer_code",
            }
        ],
        "token_sum": 50000,
    }

    mock_response = httpx.Response(
        status_code=200, 
        json=mock_response_data
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await EntryService().infer(data=inference_input)
        assert result == BrainResponse(**mock_response_data)


@pytest.mark.asyncio
async def test_infer_http_exception(inference_input):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = Response(400, json={"detail": "Bad request"})
        with pytest.raises(HTTPException):
            await EntryService().infer(data=inference_input)


@pytest.mark.asyncio
async def test_infer_json_decode_error(inference_input):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = Response(200, text="not json")
        with pytest.raises(HTTPException):
            await EntryService().infer(data=inference_input)


@pytest.mark.asyncio
async def test_infer_general_exception(inference_input):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = Exception("Unexpected error")
        with pytest.raises(HTTPException):
            await EntryService().infer(data=inference_input)


VALIDATE_TASKS_VALID_DATA = [
    (["summarise"], [Task.SUMMARISE]),
    (["practice"], [Task.PRACTICE]),
    (["practice", "summarise"], [Task.PRACTICE, Task.SUMMARISE]),
]


@pytest.mark.parametrize("tasks, expected", VALIDATE_TASKS_VALID_DATA)
def test_validate_tasks_valid(tasks, expected):
    EntryService().validate_tasks(tasks) == expected


VALIDATE_TASKS_INVALID_DATA = [("invalid_task"), ("summarise, practice")]


@pytest.mark.parametrize("tasks", VALIDATE_TASKS_INVALID_DATA)
def test_validate_tasks_invalid(tasks):
    with pytest.raises(HTTPException):
        EntryService().validate_tasks(tasks)


PREPARE_INFERENCE_DB_INPUT_VALID_DATA = [
    (
        "test_entry_id",
        {"message": "Hello"},
        BrainResponse(
            summary={"key": "value"},
            practice=[
                {
                    "language": "python",
                    "question": "question_code",
                    "answer": "answer_code",
                }
            ],
            token_sum=50000,
        ),
    ),
    (
        "test_entry_id",
        {"message": "Hello"},
        BrainResponse(
            summary={"key": "value"},
            practice=None,
            token_sum=50000,
        ),    
    ),
    (
        "test_entry_id",
        {"message": "Hello"},
        BrainResponse(
            summary=None,
            practice=[
                {
                    "language": "python",
                    "question": "question_code",
                    "answer": "answer_code",
                }
            ],
            token_sum=50000,
        ),    
    ),
]


@pytest.mark.parametrize(
    "entry_id, conversation, result", PREPARE_INFERENCE_DB_INPUT_VALID_DATA
)
def test_prepare_inference_db_input(entry_id, conversation, result):
    inference_db_input_lst = EntryService().prepare_inference_db_input_lst(
        entry_id=entry_id, conversation=conversation, result=result
    )

    for i in range(len(inference_db_input_lst)):
        assert isinstance(inference_db_input_lst[i], InferenceDbInput)
        assert inference_db_input_lst[i].entry_id == entry_id
        assert inference_db_input_lst[i].conversation == json.dumps(conversation)
        assert inference_db_input_lst[i].summary == json.dumps(result.summary)
        if result.practice is None:
            continue
        assert inference_db_input_lst[i].question == json.dumps(
            result.practice[i].get("question")
        )
        assert inference_db_input_lst[i].answer == json.dumps(
            result.practice[i].get("answer")
        )


PREPARE_INFERENCE_DB_INPUT_INVALID_DATA = [
    (
        "test_entry_id",
        {"message": "Hello"},
        123,
    ),
]


@pytest.mark.parametrize(
    "entry_id, conversation, result", PREPARE_INFERENCE_DB_INPUT_INVALID_DATA
)
def test_prepare_inference_db_input_invalid(entry_id, conversation, result):
    with pytest.raises(Exception):
        EntryService().prepare_inference_db_input_lst(
            entry_id=entry_id, conversation=conversation, result=result
        )

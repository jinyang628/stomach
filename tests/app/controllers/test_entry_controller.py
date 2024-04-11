from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.controllers.entry_controller import EntryController
from app.models.enum.task import Task
from app.models.types import BrainResponse
from app.services.entry_service import EntryService


@pytest.fixture
def mock_entry_service(mocker):
    mock_service = AsyncMock(spec=EntryService)
    mocker.patch(
        "app.controllers.entry_controller.EntryService", return_value=mock_service
    )
    return mock_service


@pytest.fixture
def mock_entry_controller(mock_entry_service):
    return EntryController(service=mock_entry_service)


@pytest.fixture
def client_with_mock_controller(mock_entry_controller):
    app = FastAPI()
    app.include_router(mock_entry_controller.router, prefix="/api/entries")
    with TestClient(app) as client:
        yield client


@pytest.fixture
def valid_payload():
    valid_payload = {
        "api_key": "test_api_key_1",
        "url": "jinyang@gmail.com",
        "tasks": [Task.SUMMARISE, Task.PRACTICE],
    }
    return valid_payload


def test_start_success(client_with_mock_controller, mock_entry_service, valid_payload):
    mock_response = BrainResponse(
        summary=None,
        practice=[
            {
                "language": "python",
                "question": "question_code",
                "answer": "answer_code",
            }
        ],
        token_sum=50000,
    )
    mock_entry_service.start_entry_process.return_value = mock_response
    response = client_with_mock_controller.post("/api/entries", json=valid_payload)
    assert response.status_code == 200
    # Compare with the output of to_dict_for_user
    assert response.json() == mock_response.to_dict_for_user()


def test_start_failure(client_with_mock_controller, mock_entry_service, valid_payload):
    mock_entry_service.start_entry_process.side_effect = Exception("Test error")

    response = client_with_mock_controller.post("/api/entries", json=valid_payload)
    assert response.status_code == 500

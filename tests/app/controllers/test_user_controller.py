from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.controllers.user_controller import UserController
from app.main import app
from app.models.enum.task import Task
from app.services.user_service import UserService

client = TestClient(app)


@pytest.fixture
def mock_user_service(mocker):
    mock_service = AsyncMock(spec=UserService)
    mocker.patch(
        "app.controllers.user_controller.UserService", return_value=mock_service
    )
    return mock_service


@pytest.fixture
def mock_user_controller(mock_user_service):
    return UserController(service=mock_user_service)


@pytest.fixture
def client_with_mock_user_controller(mock_user_controller):
    app = FastAPI()
    app.include_router(mock_user_controller.router, prefix="/api/api_keys")
    with TestClient(app) as client:
        yield client


def test_validate_api_key_successful(
    client_with_mock_user_controller, mock_user_service
):
    mock_user_service.validate_api_key.return_value = True
    response = client_with_mock_user_controller.get(
        "/api/api_keys/validate/test_api_key"
    )
    assert response.status_code == 200
    assert response.json() == {"message": "API Key successfully validated"}


def test_validate_api_key_unsuccessful(
    client_with_mock_user_controller, mock_user_service
):
    mock_user_service.validate_api_key.return_value = False
    response = client_with_mock_user_controller.get(
        "/api/api_keys/validate/invalid_api_key"
    )
    assert response.status_code == 401
    assert response.json() == {"message": "Invalid API Key"}


def test_validate_api_key_exception(
    client_with_mock_user_controller, mock_user_service
):
    mock_user_service.validate_api_key.side_effect = Exception("Test Exception")
    response = client_with_mock_user_controller.get("/api/api_keys/validate/api_key")
    assert response.status_code == 500
    assert response.json() == {"Error": "Test Exception"}


@pytest.mark.asyncio
async def test_increment_usage_successful(mock_user_controller, mock_user_service):
    # Arrange
    api_key = "test_api_key"
    tasks = [Task.PRACTICE]
    mock_user_service.increment_usage.return_value = True

    # Act
    result = await mock_user_controller.increment_usage(api_key, tasks)

    # Assert
    mock_user_service.increment_usage.assert_called_with(api_key=api_key, tasks=tasks)
    assert result is True


@pytest.mark.asyncio
async def test_increment_usage_failure(mock_user_controller, mock_user_service):
    # Arrange
    api_key = "test_api_key"
    tasks = [Task.SUMMARISE]
    mock_user_service.increment_usage.side_effect = Exception("Test Exception")

    # Act & Assert
    with pytest.raises(HTTPException):
        await mock_user_controller.increment_usage(api_key, tasks)
    mock_user_service.increment_usage.assert_called_with(api_key=api_key, tasks=tasks)

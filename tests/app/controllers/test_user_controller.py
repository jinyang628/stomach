from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.controllers.user_controller import UserController
from app.main import app
from app.models.enum.task import Task
from app.services.user_service import UserService

client = TestClient(app)


@pytest.fixture
def user_service_mock():
    return MagicMock(spec=UserService)


@pytest.fixture
def user_controller(user_service_mock):
    controller = UserController()
    controller.service = user_service_mock
    return controller


def test_validate_api_key_successful():
    with patch(
        "app.services.user_service.UserService.validate_api_key"
    ) as mock_validate:
        mock_validate.return_value = True
        response = client.get("/api/api_keys/validate/test_api_key")
        assert response.status_code == 200
        assert response.json() == {"message": "API Key successfully validated"}


def test_validate_api_key_unsuccessful():
    with patch(
        "app.services.user_service.UserService.validate_api_key"
    ) as mock_validate:
        mock_validate.return_value = False
        response = client.get("/api/api_keys/validate/invalid_api_key")
        assert response.status_code == 401
        assert response.json() == {"message": "Invalid API Key"}


def test_validate_api_key_exception():
    with patch(
        "app.services.user_service.UserService.validate_api_key"
    ) as mock_validate:
        mock_validate.side_effect = Exception("Test Exception")
        response = client.get("/api/api_keys/validate/api_key")
        assert response.status_code == 500
        assert response.json() == {"Error": "Test Exception"}


def test_increment_usage_successful(user_controller, user_service_mock):
    # Arrange
    api_key = "test_api_key"
    tasks = [Task.PRACTICE]
    user_service_mock.increment_usage.return_value = True

    # Act
    result = user_controller.increment_usage(api_key, tasks)

    # Assert
    user_service_mock.increment_usage.assert_called_with(api_key=api_key, tasks=tasks)
    assert result == True


def test_increment_usage_failure(user_controller, user_service_mock):
    # Arrange
    api_key = "test_api_key"
    tasks = [Task.SUMMARISE]  # replace with actual tasks
    user_service_mock.increment_usage.side_effect = Exception("Test Exception")

    # Act & Assert
    with pytest.raises(HTTPException):
        user_controller.increment_usage(api_key, tasks)
    user_service_mock.increment_usage.assert_called_with(api_key=api_key, tasks=tasks)

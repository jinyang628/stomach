from unittest.mock import patch

import pytest

from app.models.enum.task import Task
from app.services.user_service import UserService


@pytest.fixture
def mock_store():
    with patch("app.services.user_service.UserObjectStore") as mock:
        yield mock


@pytest.fixture
def api_key_input():
    return "test_api_key"


@pytest.fixture
def token_sum_input():
    return 50000


def test_validate_api_key(mock_store, api_key_input):
    expected_is_valid: bool = True
    mock_store.return_value.validate_api_key.return_value = expected_is_valid
    is_valid: bool = UserService().validate_api_key(api_key=api_key_input)
    assert is_valid == expected_is_valid

    mock_store.return_value.validate_api_key.assert_called_once()
    args, kwargs = mock_store.return_value.validate_api_key.call_args

    assert "api_key" in kwargs
    api_key: str = kwargs["api_key"]
    assert api_key == api_key_input


def test_validate_api_key_handles_exceptions(mock_store, api_key_input):
    mock_store.return_value.validate_api_key.side_effect = Exception("Test Exception")

    with pytest.raises(Exception) as excinfo:
        UserService().validate_api_key(api_key_input)

    assert "Test Exception" in str(excinfo.value)


def test_increment_usage_successful(mock_store, api_key_input, token_sum_input):
    mock_store.return_value.increment_usage.return_value = True
    is_incremented = UserService().increment_usage(
        api_key=api_key_input, token_sum=token_sum_input
    )

    assert is_incremented is True
    args, kwargs = mock_store.return_value.increment_usage.call_args
    assert kwargs["api_key"] == api_key_input
    assert isinstance(kwargs["usage_counter"], int)


def test_increment_usage_with_empty_tasks(api_key_input):
    with pytest.raises(ValueError) as excinfo:
        UserService().increment_usage(api_key=api_key_input, token_sum=None)
    assert "Token sum cannot be empty in the API call" in str(excinfo.value)


def test_increment_usage_handles_exceptions(mock_store, api_key_input, token_sum_input):
    mock_store.return_value.increment_usage.side_effect = Exception("Test Exception")
    with pytest.raises(Exception) as excinfo:
        UserService().increment_usage(api_key=api_key_input, token_sum=token_sum_input)
    assert "Test Exception" in str(excinfo.value)

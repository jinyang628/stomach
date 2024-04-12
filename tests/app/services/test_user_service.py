from unittest.mock import patch

import pytest

from app.services.user_service import UserService


@pytest.fixture
def mock_user_store():
    with patch("app.services.user_service.UserObjectStore") as mock:
        yield mock


@pytest.fixture
def api_key_input():
    return "test_api_key"


@pytest.fixture
def token_sum_input():
    return 50000


def test_validate_api_key(mock_user_store, api_key_input):
    expected_is_valid: bool = True
    mock_user_store.return_value.validate_api_key.return_value = expected_is_valid
    is_valid: bool = UserService().validate_api_key(api_key=api_key_input)
    assert is_valid == expected_is_valid

    mock_user_store.return_value.validate_api_key.assert_called_once()
    args, kwargs = mock_user_store.return_value.validate_api_key.call_args

    assert "api_key" in kwargs
    api_key: str = kwargs["api_key"]
    assert api_key == api_key_input


def test_validate_api_key_handles_exceptions(mock_user_store, api_key_input):
    mock_user_store.return_value.validate_api_key.side_effect = Exception("Test Exception")

    with pytest.raises(Exception) as excinfo:
        UserService().validate_api_key(api_key_input)

    assert "Test Exception" in str(excinfo.value)


def test_increment_usage_successful(mock_user_store, api_key_input, token_sum_input):
    mock_user_store.return_value.increment_usage.return_value = True
    is_incremented = UserService().increment_usage(
        api_key=api_key_input, token_sum=token_sum_input
    )

    assert is_incremented is True
    args, kwargs = mock_user_store.return_value.increment_usage.call_args
    assert kwargs["api_key"] == api_key_input
    assert isinstance(kwargs["usage_counter"], int)


def test_increment_usage_with_empty_tasks(api_key_input):
    with pytest.raises(ValueError) as excinfo:
        UserService().increment_usage(api_key=api_key_input, token_sum=None)
    assert "Token sum cannot be empty in the API call" in str(excinfo.value)


def test_increment_usage_handles_exceptions(mock_user_store, api_key_input, token_sum_input):
    mock_user_store.return_value.increment_usage.side_effect = Exception("Test Exception")
    with pytest.raises(Exception) as excinfo:
        UserService().increment_usage(api_key=api_key_input, token_sum=token_sum_input)
    assert "Test Exception" in str(excinfo.value)

def test_is_within_limit_true(mock_user_store, api_key_input):
    # Setup mock to return True, indicating the user is within the limit
    mock_user_store.return_value.is_within_limit.return_value = True

    # Instantiate the service and call the method
    is_within_limit = UserService().is_within_limit(api_key=api_key_input)

    # Assert that the function returns True
    assert is_within_limit is True
    mock_user_store.return_value.is_within_limit.assert_called_once_with(api_key=api_key_input)

def test_is_within_limit_false(mock_user_store, api_key_input):
    # Setup mock to return False, indicating the user is not within the limit
    mock_user_store.return_value.is_within_limit.return_value = False

    # Call the method
    is_within_limit = UserService().is_within_limit(api_key=api_key_input)

    # Assert that the function returns False
    assert is_within_limit is False
    mock_user_store.return_value.is_within_limit.assert_called_once_with(api_key=api_key_input)

def test_is_within_limit_handles_exceptions(mock_user_store, api_key_input):
    # Setup mock to raise an exception
    mock_user_store.return_value.is_within_limit.side_effect = Exception("Database failure")

    # Assert that an appropriate exception is raised when calling the method
    with pytest.raises(Exception) as exc_info:
        UserService().is_within_limit(api_key=api_key_input)

    assert "Database failure" in str(exc_info.value)
    mock_user_store.return_value.is_within_limit.assert_called_once_with(api_key=api_key_input)
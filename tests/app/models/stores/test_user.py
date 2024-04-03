from typing import Union, get_args

import pytest

from app.models.stores.user import USER_VERSION, User
from app.models.utils import sql_value_to_typed_value

# Data for testing the local method
USER_LOCAL_VALID_DATA = [
    ("jinyang", "email@example.com", "api_key_1"),
    ("shawn", "another_email@example.com", "api_key_2"),
]


@pytest.mark.parametrize("name, email, api_key", USER_LOCAL_VALID_DATA)
def test_user_local_valid(name, email, api_key):
    user = User.local(name=name, email=email, api_key=api_key)
    assert user.version == USER_VERSION
    assert user.name == name
    assert user.email == email
    assert user.api_key == api_key


USER_LOCAL_INVALID_DATA = [
    (123, "jinyang@gmail.com", "api_key"),  # Invalid name
    ("jinyang", 123, "api_key"),  # Invalid email
    ("jinyang", "email@example.com", 123),  # Empty API key
]


@pytest.mark.parametrize("name, email, api_key", USER_LOCAL_INVALID_DATA)
def test_user_local_invalid(name, email, api_key):
    with pytest.raises(ValueError):
        User.local(name=name, email=email, api_key=api_key)


# Data for testing the remote method
USER_REMOTE_VALID_DATA = [
    {
        "id": "1",
        "version": "1",
        "name": "jinyang",
        "email": "email1@example.com",
        "api_key": "api_key_1",
        "usage": "0",
        "created_at": "2021-01-01 00:00:00",
        "updated_at": "2021-01-01 00:00:00",
    },
]


@pytest.mark.parametrize("kwargs", USER_REMOTE_VALID_DATA)
def test_user_remote_valid(kwargs):
    user = User.remote(**kwargs)
    for key, value in kwargs.items():
        if key in User.__annotations__:
            expected_type = User.__annotations__[key]
            # Handle Union types (like Optional fields)
            if (
                hasattr(expected_type, "__origin__")
                and expected_type.__origin__ is Union
            ):
                # Assuming we always have one type and None in Union
                non_none_types = [
                    t for t in get_args(expected_type) if t is not type(None)
                ]
                assert len(non_none_types) == 1  # Ensuring it's a simple Optional type
                expected_type = non_none_types[0]
            else:
                expected_type = expected_type
            expected_value = sql_value_to_typed_value(
                dict=kwargs, key=key, type=expected_type
            )
            assert getattr(user, key) == expected_value
        else:
            pytest.fail(f"Field '{key}' not found in User model")


USER_REMOTE_INVALID_DATA = [
    {
        "id": "not_an_int",
        "name": "jinyang",
        "version": "1",
        "email": "email@example.com",
        "api_key": "api_key",
    },  # Invalid id
    {"email": "email@example.com", "api_key": "api_key"},  # Missing version
]


@pytest.mark.parametrize("kwargs", USER_REMOTE_INVALID_DATA)
def test_user_remote_invalid(kwargs):
    with pytest.raises(Exception):
        User.remote(**kwargs)

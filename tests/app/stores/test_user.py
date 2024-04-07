from datetime import datetime
from typing import List
from unittest.mock import patch

import pytest

from app.models.stores.user import User
from app.stores.user import UserObjectStore


@pytest.fixture
def user_store():
    return UserObjectStore()


@pytest.fixture
def sample_user_remote():
    return User(
        id=0,
        version=1,
        name="shawn",
        email="jinyang@gmail.com",
        api_key="api_key_1",
        usage=0,
        created_at="2024-04-06 17:50:51",
        updated_at="2024-04-06 17:50:51",
    )


def test_insert_get_update_delete():
    store = UserObjectStore()
    object_1 = User.local(
        name="jinyang",
        email="jinyang0220@gmail.com",
        api_key="test_api_key_1",
    )
    object_2 = User.local(
        name="jinyang",
        email="jinyang0220@gmail.com",
        api_key="test_api_key_2",
    )
    inserted_ids: List[int] = store.insert(users=[object_1, object_2])
    assert len(inserted_ids) == 2

    objs = store.get_by_ids(ids=inserted_ids)
    assert len(objs) == 2

    obj_1 = objs[0]
    assert obj_1.id == inserted_ids[0]
    assert obj_1.name == object_1.name
    assert obj_1.version == object_1.version
    assert obj_1.email == object_1.email
    assert obj_1.api_key == object_1.api_key
    obj_2 = objs[1]
    assert obj_2.id == inserted_ids[1]
    assert obj_2.name == object_2.name
    assert obj_2.version == object_2.version
    assert obj_2.email == object_2.email
    assert obj_2.api_key == object_2.api_key

    obj_1.email = "siyuan@hotmail.com"
    success = store.update(users=[obj_1])
    assert success

    updated_objects = store.get_by_ids(ids=[obj_1.id])
    assert len(updated_objects) == 1
    assert updated_objects[0].email == "siyuan@hotmail.com"

    success = store.delete(ids=inserted_ids)
    assert success


def test_increment_usage_successful(user_store, sample_user_remote):
    mock_user_data = sample_user_remote.model_dump()
    with patch.object(
        user_store._store,
        "get_rows_by_matching_condition",
        return_value=[mock_user_data],
    ) as mock_get, patch.object(
        user_store._store, "convert_row_to_dict", return_value=mock_user_data
    ) as mock_convert, patch.object(
        user_store, "update", return_value=True
    ) as mock_update:

        result = user_store.increment_usage(api_key="valid_api_key", usage_counter=5)
        assert result
        mock_get.assert_called_once_with(
            column_to_match="api_key", matching_value="valid_api_key"
        )
        mock_convert.assert_called_once_with(sample_user_remote.model_dump(), User)
        sample_user_remote.usage += 5
        mock_update.assert_called_once_with(users=[sample_user_remote])


def test_increment_usage_invalid_api_key(user_store):
    with patch.object(
        user_store._store, "get_rows_by_matching_condition", return_value=[]
    ):
        with pytest.raises(Exception) as excinfo:
            user_store.increment_usage(api_key="invalid_api_key", usage_counter=5)
        assert "API call is made even though the API key is invalid" in str(
            excinfo.value
        )


def test_increment_usage_database_exception(user_store, sample_user_remote):
    with patch.object(
        user_store._store,
        "get_rows_by_matching_condition",
        side_effect=Exception("DB Error"),
    ):
        with pytest.raises(Exception) as excinfo:
            user_store.increment_usage(api_key="valid_api_key", usage_counter=5)
        assert "DB Error" in str(excinfo.value)

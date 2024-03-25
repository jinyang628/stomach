from typing import List

import pytest

from app.models.stores.entry import Entry
from app.stores.entry import EntryObjectStore


@pytest.fixture
def store():
    return EntryObjectStore()


def test_insert_get_update_delete():
    store = EntryObjectStore()
    object_1 = Entry.local(api_key="test_api_key", url="test_url")
    object_2 = Entry.local(
        api_key="test_api_key_2",
        url="test_url_2",
    )
    inserted_ids: List[int] = store.insert(
        entries=[object_1, object_2], return_column="id"
    )
    assert len(inserted_ids) == 2

    objs = store.get(ids=inserted_ids)
    assert len(objs) == 2

    obj_1 = objs[0]
    assert obj_1.id == inserted_ids[0]
    assert obj_1.version == object_1.version
    assert obj_1.url == object_1.url
    assert obj_1.api_key == object_1.api_key
    assert obj_1.entry_id == object_1.entry_id
    obj_2 = objs[1]
    assert obj_2.id == inserted_ids[1]
    assert obj_2.version == object_2.version
    assert obj_2.url == object_2.url
    assert obj_2.api_key == object_2.api_key
    assert obj_2.entry_id == object_2.entry_id

    obj_1.url = "test_url_1_updated"
    success = store.update(entries=[obj_1])
    assert success

    updated_objects = store.get(ids=[obj_1.id])
    assert len(updated_objects) == 1
    assert updated_objects[0].url == "test_url_1_updated"

    success = store.delete(ids=inserted_ids)
    assert success

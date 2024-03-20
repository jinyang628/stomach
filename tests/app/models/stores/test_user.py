from typing import List
from app.models.stores.user import User
from app.stores.user import UserObjectStore


def test_insert_get_update_delete():
    store = UserObjectStore()
    object_1 = User.local(
        version=1,
        email="jinyang0220@gmail.com",
        api_key="test_api_key_1",
    )
    object_2 = User.local(
        version=1,
        email="jinyang0220@gmail.com",
        api_key="test_api_key_2",
    )
    inserted_ids: List[int] = store.insert(users=[object_1, object_2])
    assert len(inserted_ids) == 2

    objs = store.get(ids=inserted_ids)
    assert len(objs) == 2

    obj_1 = objs[0]
    assert obj_1.id == inserted_ids[0]
    assert obj_1.version == object_1.version
    assert obj_1.email == object_1.email
    assert obj_1.api_key == object_1.api_key
    obj_2 = objs[1]
    assert obj_2.id == inserted_ids[1]
    assert obj_2.version == object_2.version
    assert obj_2.email == object_2.email
    assert obj_2.api_key == object_2.api_key

    obj_1.email = "siyuan@hotmail.com"
    success = store.update(users=[obj_1])
    assert success

    updated_objects = store.get(ids=[obj_1.id])
    assert len(updated_objects) == 1
    assert updated_objects[0].email == "siyuan@hotmail.com"

    success = store.delete(ids=inserted_ids)
    assert success

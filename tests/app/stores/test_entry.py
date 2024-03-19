from typing import List
from app.models.entry import Entry
from app.stores.entry import EntryObjectStore


def test_insert_get():
    store = EntryObjectStore()
    object_1 = Entry.local(
        version=1,
        entry_id="test_entry_id",
        api_key="test_api_key",
        url="test_url"
    )
    object_2 = Entry.local(
        version=1,
        entry_id="test_entry_id_2",
        api_key="test_api_key_2",
        url="test_url_2"
    )
    inserted_ids: List[int] = store.insert(entries=[object_1, object_2])
    assert len(inserted_ids) == 2
    
    objs = store.get(ids=inserted_ids)
    assert len(objs) == 2
    
    obj_1 = objs[0]
    assert obj_1.id == inserted_ids[0]
    assert obj_1.url == object_1.url
    assert obj_1.version == object_1.version
    assert obj_1.api_key == object_1.api_key
    assert obj_1.entry_id == object_1.entry_id    
    obj_2 = objs[1]
    assert obj_2.id == inserted_ids[1]
    assert obj_2.version == object_2.version
    assert obj_2.url == object_2.url
    assert obj_2.api_key == object_2.api_key
    assert obj_2.entry_id == object_2.entry_id
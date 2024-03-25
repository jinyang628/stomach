from typing import List
from app.models.stores.inference import Inference
from app.stores.inference import InferenceObjectStore
import json


def test_insert_get_update_delete():
    store = InferenceObjectStore()
    object_1 = Inference.local(
        entry_id="test_entry_id_1",
        conversation=json.dumps(
            {
                "title": "test_title",
                "UserMessage1": "test_user_message_1",
                "AssistantMessage1": "test_assistant_message_1",
            }
        ),
        summary="test_summary",
        practice=None,
    )
    object_2 = Inference.local(
        entry_id="test_entry_id_2",
        conversation=json.dumps(
            {
                "title": "test_title",
                "UserMessage1": "test_user_message_1",
                "AssistantMessage1": "test_assistant_message_1",
            }
        ),
        summary=None,
        practice="test_exercise",
    )
    inserted_ids: List[int] = store.insert(inferences=[object_1, object_2])
    assert len(inserted_ids) == 2

    objs = store.get(ids=inserted_ids)
    assert len(objs) == 2

    obj_1 = objs[0]
    assert obj_1.id == inserted_ids[0]
    assert obj_1.version == object_1.version
    assert obj_1.entry_id == object_1.entry_id
    assert obj_1.conversation == object_1.conversation
    assert obj_1.summary == object_1.summary
    assert obj_1.practice == object_1.practice

    obj_2 = objs[1]
    assert obj_2.id == inserted_ids[1]
    assert obj_2.version == object_2.version
    assert obj_2.entry_id == object_2.entry_id
    assert obj_2.conversation == object_2.conversation
    assert obj_2.summary == object_2.summary
    assert obj_2.practice == object_2.practice

    obj_1.summary = "test_summary_updated"
    success = store.update(inferences=[obj_1])
    assert success

    updated_objects = store.get(ids=[obj_1.id])
    assert len(updated_objects) == 1
    assert updated_objects[0].summary == "test_summary_updated"

    success = store.delete(ids=inserted_ids)
    assert success

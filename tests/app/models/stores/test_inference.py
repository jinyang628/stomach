from typing import Union, get_args

import pytest

from app.models.stores.inference import INFERENCE_VERSION, Inference
from app.models.utils import sql_value_to_typed_value

INFERENCE_LOCAL_VALID_DATA = [
    (
        "entry_id_1",
        "Test conversation 1",
        "Test summary 1",
        "Test summary chunk 1",
        "Test question 1",
        "Test answer 1",
        "Test language 1"
    ),
    ("entry_id_2", "Test conversation 2", None, None, None, None, None),
]


@pytest.mark.parametrize(
    "entry_id, conversation, summary, summary_chunk, question, answer, language", INFERENCE_LOCAL_VALID_DATA
)
def test_inference_local_valid(entry_id, conversation, summary, summary_chunk, question, answer, language):
    inference = Inference.local(entry_id, conversation, summary, summary_chunk, question, answer, language)
    assert inference.version == INFERENCE_VERSION
    assert inference.entry_id == entry_id
    assert inference.conversation == conversation
    assert inference.summary == summary
    assert inference.summary_chunk == summary_chunk
    assert inference.question == question
    assert inference.answer == answer
    assert inference.language == language


INFERENCE_LOCAL_INVALID_DATA = [
    (None, "Test conversation", None, None, None, None, None),  # Missing entry_id
    ("entry_id", None, None, None, None, None, None),  # Missing conversation
]


@pytest.mark.parametrize(
    "entry_id, conversation, summary, summary_chunk, question, answer, language", INFERENCE_LOCAL_INVALID_DATA
)
def test_inference_local_invalid(entry_id, conversation, summary, summary_chunk, question, answer, language):
    with pytest.raises(ValueError):  # Or the specific error your code raises
        Inference.local(entry_id, conversation, summary, summary_chunk, question, answer, language)


INFERENCE_REMOTE_VALID_DATA = [
    {
        "id": "1",
        "version": "1",
        "entry_id": "entry_id_1",
        "conversation": "Test conversation 1",
        "summary": "Test summary 1",
        "summary_chunk": "Test summary chunk 1",
        "question": "Test question 1",
        "answer": "Test answer 1",
        "language": "Test language 1"
    },
    {
        "id": "2",
        "version": "1",
        "entry_id": "entry_id_2",
        "conversation": "Test conversation 2",
        "summary": None,
        "summary_chunk": None,
        "question": None,
        "answer": None,
        "language": None
    },
]


@pytest.mark.parametrize("kwargs", INFERENCE_REMOTE_VALID_DATA)
def test_inference_remote_valid(kwargs):
    inference = Inference.remote(**kwargs)
    for key, value in kwargs.items():
        if key in Inference.__annotations__:
            expected_type = Inference.__annotations__[key]
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
            assert getattr(inference, key) == expected_value
        else:
            pytest.fail(f"Field '{key}' not found in Inference model")


INFERENCE_REMOTE_INVALID_DATA = [
    {
        "id": "not_an_int",
        "version": "1",
        "entry_id": "entry_id_1",
        "conversation": "Test conversation 1",
    },  # Invalid id
    {
        "id": "1",
        "version": "not_an_int",
        "entry_id": "entry_id_2",
        "conversation": "Test conversation 2",
    },  # Invalid version
    {
        "id": "3",
        "version": "1",
        "conversation": "Test conversation 3",
    },  # Missing entry_id
]


@pytest.mark.parametrize("kwargs", INFERENCE_REMOTE_INVALID_DATA)
def test_inference_remote_invalid(kwargs):
    with pytest.raises(Exception):
        Inference.remote(**kwargs)

import pytest
from app.models.stores.entry import Entry, ENTRY_VERSION

import unittest.mock as mock

ENTRY_LOCAL_CONSTRUCTOR_VALID_DATA = [
    ("api_key_1", "https://example.com/1", "entry_id_1", "entry_id_1"),  # Provided entry_id
    ("api_key_2", "https://example.com/2", None, "expected_generated_id_2"),  # Generated entry_id
]

@pytest.mark.parametrize("api_key, url, entry_id, expected_entry_id", ENTRY_LOCAL_CONSTRUCTOR_VALID_DATA)
@mock.patch('app.models.stores.entry.generate_identifier', return_value="expected_generated_id_2")
def test_entry_local(mock_generate_identifier, api_key, url, entry_id, expected_entry_id):
    entry = Entry.local(api_key=api_key, url=url, entry_id=entry_id)

    assert entry.version == ENTRY_VERSION
    assert entry.entry_id == expected_entry_id
    assert entry.api_key == api_key
    assert entry.url == url
    
ENTRY_LOCAL_CONSTRUCTOR_INVALID_DATA = [
    (None, "https://example.com", None, ValueError),  # None api_key
    ("api_key", None, None, ValueError),             # None url
]

@pytest.mark.parametrize("api_key, url, entry_id, expected_exception", ENTRY_LOCAL_CONSTRUCTOR_INVALID_DATA)
def test_entry_local_invalid(api_key, url, entry_id, expected_exception):
    with pytest.raises(expected_exception):
        Entry.local(api_key=api_key, url=url, entry_id=entry_id)

ENTRY_REMOTE_CONSTRUCTOR_VALID_DATA = [
    ({"id": "123", "version": "1", "entry_id": "entry_id_1", "api_key": "api_key_1", "url": "https://example.com/1"})
]
@pytest.mark.parametrize("input_data", ENTRY_REMOTE_CONSTRUCTOR_VALID_DATA)
@mock.patch('app.models.stores.entry.sql_value_to_typed_value')
def test_entry_remote(mock_sql_to_typed, input_data):
    mock_sql_to_typed.side_effect = lambda dict, key, type: dict.get(key)
    entry = Entry.remote(**input_data)
    assert isinstance(entry, Entry)
    
ENTRY_REMOTE_CONSTURCTOR_INVALID_DATA = [
    ({"id": "not_a_number", "version": "1", "entry_id": "entry_id_2", "api_key": "api_key_2", "url": "https://example.com/2"}),
    ({"id": "123", "version": "not a number", "entry_id": "entry_id_2", "api_key": "api_key_2", "url": "https://example.com/2"}),
    ({"id": "123", "version": "1", "entry_id": 123, "api_key": "api_key_2", "url": "https://example.com/2"}),
    ({"id": "123", "version": "1", "entry_id": "entry_id_4", "api_key": 123, "url": "https://example.com/2"}),
    ({"id": "123", "version": "1", "entry_id": "entry_id_4", "api_key": "api_key_5", "url": 123}),
]
@pytest.mark.parametrize("input_data", ENTRY_REMOTE_CONSTURCTOR_INVALID_DATA)
@mock.patch('app.models.stores.entry.sql_value_to_typed_value')
def test_entry_remote_invalid_data(mock_sql_to_typed, input_data):
    mock_sql_to_typed.side_effect = lambda dict, key, type: dict.get(key)
    with pytest.raises(ValueError):
        entry = Entry.remote(**input_data)
        assert isinstance(entry, Entry)

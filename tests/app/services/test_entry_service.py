import pytest
from unittest.mock import patch
from app.models.enum.task import Task
from app.models.stores.entry import Entry
from app.services.entry_service import EntryService, EntryDbInput

@pytest.fixture
def mock_store():
    with patch('app.services.entry_service.EntryObjectStore') as mock:
        yield mock

@pytest.fixture
def entry_input():
    return EntryDbInput(api_key="test_api_key", url="http://test.url", tasks=[Task.SUMMARISE])

async def test_post(mock_store, entry_input):
    expected_entry_id: str = "test_entry_id"
    mock_store.return_value.insert.return_value = expected_entry_id
    entry_id: str = await EntryService().post(input=entry_input, return_column="id")
    assert entry_id == expected_entry_id

    mock_store.return_value.insert.assert_called_once()
    args, kwargs = mock_store.return_value.insert.call_args
    assert 'entries' in kwargs
    entries = kwargs['entries']
    assert len(entries) == 1  # One entry should be passed
    assert isinstance(entries[0], Entry)
    assert entries[0].api_key == entry_input.api_key
    assert entries[0].url == entry_input.url

async def test_post_entry_handles_exceptions(mock_store, entry_input):
    mock_store.return_value.insert.side_effect = Exception("Test Exception")
    
    with pytest.raises(Exception) as excinfo:
        await EntryService().post(input=entry_input, return_column="id")
    
    assert "Test Exception" in str(excinfo.value)

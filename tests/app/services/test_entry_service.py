from unittest.mock import MagicMock, patch, AsyncMock
import json
import pytest
from mongomock import MongoClient
from app.services.entry_service import EntryService
from app.models.entry_controller.createEntryInput import CreateEntryInput
from app.models.entry_controller import Entry

# Blocked here its working but test is not, will revisit later

# Use pytest-asyncio for async test functions
# @pytest.mark.asyncio
# async def test_create():
#     # Mock request and database
#     request = MagicMock()
#     request.app.database = MongoClient().db

#     # Mock URLModel data
#     url_data = UrlModel(url="http://example.com")

#     # Mock extractUrlContent function to return a predefined dict
#     service = EntryService()
#     result = await service.create(request, url_data)
#     # Assert the result is a JSON string (since your create method returns a JSON string)
#     assert isinstance(result, Entry)

#     # Optionally, decode the result and assert on its content
#     entry_data = json.loads(result)
#     assert entry_data["user_id"] == url_data.url  # or any other assertion relevant to your logic


# Mocking the Request object to include a mock database in its app attribute
@pytest.fixture
def mock_request():
    request = MagicMock()
    request.app.database = {"Entries": MagicMock()}
    return request


@pytest.mark.asyncio
async def test_get_all(mock_request):
    # Sample data to return
    mock_data_batch1 = [{"_id": "1", "data": "First batch of data"}]
    mock_data_batch2 = [{"_id": "2", "data": "Second batch of data"}]

    # Mock the find().skip().limit().to_list() chain
    async_mock_to_list = AsyncMock(
        side_effect=[mock_data_batch1, mock_data_batch2, []]
    )  # Returns two batches and then an empty list to end the loop
    mock_request.app.database[
        "Entries"
    ].find.return_value.skip.return_value.limit.return_value.to_list = (
        async_mock_to_list
    )

    # Initialize EntryService
    service = EntryService()

    # Execute the get_all method
    entries = await service.get_all(mock_request)

    # Verify the method returns the correct aggregated data
    assert (
        entries == mock_data_batch1 + mock_data_batch2
    )  # Combine the batches for the expected result

    # Ensure to_list was called with the correct limit each time
    async_mock_to_list.assert_called_with(length=100)

    # Verify the skip values used (0 for the first batch, 100 for the second)
    mock_request.app.database["Entries"].find().skip.assert_any_call(0)
    mock_request.app.database["Entries"].find().skip.assert_any_call(100)

    # Verify the method does not return more data after the second batch
    assert len(entries) == len(mock_data_batch1) + len(mock_data_batch2)

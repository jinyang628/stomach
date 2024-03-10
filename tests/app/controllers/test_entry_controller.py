import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.controllers.entry_controller import entry_controller_router
from app.models.entry import Entry
from app.models.url import UrlModel
from unittest.mock import AsyncMock, patch

# Setup FastAPI app instance for testing
app = FastAPI()
app.include_router(entry_controller_router)

# Example test data
test_entry_data = {"user_id": "test_user", "messages": {"title": "Test Entry"}}
test_entry = Entry(**test_entry_data)
test_entry_list = [test_entry]
test_url_data = UrlModel(url="http://example.com")

@pytest.mark.asyncio
async def test_list_entries():
    with patch('app.services.entry_service.EntryService.get_all', new=AsyncMock(return_value=test_entry_list)):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == [test_entry.dict()]

@pytest.mark.asyncio
async def test_create_entry():
    with patch('app.services.entry_service.EntryService.create', new=AsyncMock(return_value=test_entry)):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/", json=test_url_data.dict())
        assert response.status_code == 200
        assert response.json() == test_entry.dict()

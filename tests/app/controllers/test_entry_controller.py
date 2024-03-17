import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status
from app.controllers.entry_controller import entry_controller_router
from app.models.entry_controller import Entry
from app.models.entry_controller.createEntryInput import CreateEntryInput
from unittest.mock import AsyncMock, patch
import os
from dotenv import load_dotenv

load_dotenv()

BRAIN_API_URL: str = os.getenv("BRAIN_API_URL")

# Setup FastAPI app instance for testing
app = FastAPI()
app.include_router(entry_controller_router)

# Example test data
test_entry_data = {"user_id": "test_user", "messages": {"title": "Test Entry"}}
test_entry = Entry(**test_entry_data)
test_entry_list = [test_entry]
test_url_data = CreateEntryInput(url="http://example.com")


@pytest.mark.asyncio
async def test_list_entries():
    with patch(
        "app.services.entry_service.EntryService.get_all",
        new=AsyncMock(return_value=test_entry_list),
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == [test_entry.model_dump()]


@pytest.mark.asyncio
async def test_create_entry():
    # Directly return the dictionary expected, no need to json.dumps() here
    with patch(
        "app.services.entry_service.EntryService.create",
        new=AsyncMock(return_value=test_entry_data),  # Return the dictionary directly
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Assuming test_url_data is defined and valid
            # TODO: Aaron, please look at main.py in brain repo. The input to the /api/infer endpoint must follow the InferInputModel shape. If not, an internal server error 500 will be thrown. Y
            response = await ac.post("/", json=test_url_data.model_dump())
            print(response.json())

        assert response.status_code == status.HTTP_200_OK

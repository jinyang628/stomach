from typing import Any, List
import logging
from fastapi import APIRouter, HTTPException, Request
from app.api.inference._post import _post
from app.models.entry_controller.inferenceInput import InferenceInput
from app.models.entry_controller.task import Task
from app.services.entry_service import EntryService
from app.models.entry_controller.entry import Entry
from app.models.entry_controller.createEntryInput import CreateEntryInput

from app.services.entry_service import EntryService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EntryController:
    def __init__(self):
        self._router = APIRouter()
        self._service = EntryService()
        self.setup_routes()

    def setup_routes(self):
        service = self._service

        @self._router.get("/", response_model=List[Entry])
        async def list_entries(request: Request) -> List[Entry]:
            entries = await service.get_all(request)
            return entries

        @self._router.post("/")
        async def create_entry(data: CreateEntryInput, request: Request) -> dict[str, Any]:
            
            try:
                # THIS dict[str, Any] is a quick fix, we we need to split this out into id, user_id, messages, etc wrapped under a proper class.
                entry: EntryResponse = await service.create(request, data)
                tasks: list[Task] = data.tasks
                
                # After changing the shape of entry, please update the InferenceInput shape too
                input: InferenceInput = InferenceInput(entry=entry, tasks=tasks)
                try:
                    # Even though we don't use the result, we await the response to ensure there's no error (e.g. link is invalid)
                    await _post(data=input)
                    # If inference succeeds, the following message will be returned. No content is returned at this juncture.
                    return {"message": "Successfully completed inference"}
                except Exception as e:
                    logger.error("Error in inference: %s", str(e))
                    raise HTTPException(status_code=500, detail=str(e))
            except Exception as e:
                logger.error("Error in creating entry: %s", str(e))
                raise HTTPException(status_code=500, detail=str(e))


# Create an instance of ApiController
entry_controller_router = EntryController().router

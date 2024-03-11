from typing import List
import logging
from fastapi import APIRouter, Request
from app.api.infer import infer
from app.services.entry_service import EntryService
from app.models.entry import Entry
from app.models.url import UrlModel
from app.services.entry_service import EntryService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EntryController:
    def __init__(self):
        self.router = APIRouter()
        self.service = EntryService()
        self.setup_routes()

    def setup_routes(self):
        router = self.router
        service = self.service

        @router.get("/", response_model=List[Entry])
        async def list_entries(request: Request) -> List[Entry]:
            entries = await service.get_all(request)
            return entries

        @router.post("/")
        async def create_entry(data: UrlModel, request: Request) -> dict[str, str]:
            try:
                entry: dict[str, str] = await service.create(request, data)
                try:
                    response_data = await infer(entry)
                    return response_data
                except Exception as e:
                    logger.error("Error in inference: %s", str(e))
                    return {"Error": str(e)}, 500
            except Exception as e:
                logger.error("Error in creating entry: %s", str(e))
                return {"Error": str(e)}, 500


# Create an instance of ApiController
entry_controller_router = EntryController().router

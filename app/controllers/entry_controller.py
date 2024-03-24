from fastapi import APIRouter, HTTPException, Request
from app.models.types import _PostEntriesInput
from app.services.entry_service import EntryService
import logging

log = logging.getLogger(__name__)

router = APIRouter()

class EntryController:
    def __init__(self):
        self.router = APIRouter()
        self.service = EntryService()
        self.setup_routes()
    
    def setup_routes(self):
        
        router = self.router
        service = self.service
                
        @router.post("")
        async def start(input: _PostEntriesInput):
            try:
                entry_id: str = service.post_entry(input=input, return_column="entry_id")
                return {"entry_id": entry_id}
            except Exception as e:
                log.error("Error: %s", str(e))
                raise HTTPException(status_code=500, detail=str(e))

entry_controller_router = EntryController().router

                

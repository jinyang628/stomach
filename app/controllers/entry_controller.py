import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.models.types import EntryDbInput
from app.services.entry_service import EntryService

log = logging.getLogger(__name__)

router = APIRouter()


class EntryController:
    
    def __init__(self, service: EntryService):
        self.router = APIRouter()
        self.service = service
        self.setup_routes()

    def setup_routes(self):

        router = self.router
        
        @router.post("")
        async def start(input: EntryDbInput) -> JSONResponse:
            try:
                result: dict[str, Any] = await self.service.start_entry_process(input=input)
                return JSONResponse(status_code=200, content=result)
            except Exception as e:
                log.error("Error starting in entry_controller.py: %s", str(e))
                raise HTTPException(status_code=500, detail=str(e))        
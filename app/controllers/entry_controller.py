import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.exceptions.exception import (DatabaseError, PipelineError,
                                      UsageLimitExceededError)
from app.models.types import BrainResponse, EntryDbInput
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
            """Marks the start of the pipeline when the user submits a ShareGPT link.

            Args:
                input (EntryDbInput): The input data to be stored in the entry table

            Returns:
                JSONResponse: The inference response from Brain to be passed back to Fingers.
            """
            try:
                brain_response: BrainResponse = await self.service.start_entry_process(
                    input=input
                )
                return JSONResponse(
                    status_code=200, content=brain_response.to_dict_for_user()
                )
            except UsageLimitExceededError as e:
                log.error("Usage limit exceeded: %s", str(e))
                raise UsageLimitExceededError(message=str(e))
            except DatabaseError as e:
                log.error("Database error: %s", str(e))
                raise DatabaseError(message=str(e)) from e
            except PipelineError as e:
                log.error("Error in entry_controller.py: %s", str(e))
                raise PipelineError(message=str(e)) from e
            except Exception as e:
                log.error("Unexpected error in entry_controller.py: %s", str(e))
                raise HTTPException(status_code=500, detail=str(e)) from e

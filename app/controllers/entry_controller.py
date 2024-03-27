import asyncio
import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.controllers.inference_controller import InferenceController
from app.models.types import EntryDbInput, InferenceDbInput, InferenceInput
from app.services.entry_service import EntryService

log = logging.getLogger(__name__)

router = APIRouter()


class EntryController:
    def __init__(self):
        self.router = APIRouter()
        self.service = EntryService()
        self.inference_controller = InferenceController()
        self.setup_routes()

    def setup_routes(self):

        router = self.router
        service = self.service

        @router.post("")
        async def start(input: EntryDbInput) -> dict[str, str]:
            try:

                async def post() -> str:
                    try:
                        entry_ids: list[str] = await service.post(
                            data=[input], return_column="entry_id"
                        )
                        return entry_ids[0]
                    except Exception as e:
                        log.error(
                            "Error posting to entry db in entry_controller.py: %s",
                            str(e),
                        )
                        raise HTTPException(status_code=500, detail=str(e)) from e

                async def extract_url_content() -> dict[str, str]:
                    jsonified_conversation: dict[str, str] = (
                        await service.extract_url_content(url=input.url)
                    )
                    return jsonified_conversation

                entry_id_task = asyncio.create_task(post())
                conversation_task = asyncio.create_task(extract_url_content())

                service.validate_tasks(input.tasks)

                jsonified_conversation: dict[str, str] = await conversation_task
                inference_input = InferenceInput(
                    conversation=jsonified_conversation, tasks=input.tasks
                )

                try:
                    result: dict[str, Any] = await service.infer(data=inference_input)
                except Exception as e:
                    log.error(
                        "Error posting infer request to BRAIN in entry_controller.py: %s",
                        str(e),
                    )
                    raise HTTPException(status_code=500, detail=str(e)) from e

                entry_id: str = await entry_id_task

                inference_db_input: InferenceDbInput = (
                    service.prepare_inference_db_input(
                        entry_id=entry_id,
                        conversation=jsonified_conversation,
                        result=result,
                    )
                )

                try:
                    await self.inference_controller.post(data=inference_db_input)
                except Exception as e:
                    log.error(
                        "Error posting to inference db in entry_controller.py: %s",
                        str(e),
                    )
                    raise HTTPException(status_code=500, detail=str(e)) from e

                return JSONResponse(status_code=200, content=result)
            except Exception as e:
                log.error("Error starting in entry_controller.py: %s", str(e))
                raise HTTPException(status_code=500, detail=str(e)) from e


entry_controller_router = EntryController().router

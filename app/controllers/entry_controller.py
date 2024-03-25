import asyncio
import json
import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.controllers.inference_controller import InferenceController
from app.models.enum.task import Task
from app.models.logic.conversation import Conversation
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
                            input=[input], return_column="entry_id"
                        )
                        return entry_ids[0]
                    except Exception as e:
                        log.error(
                            "Error posting to entry db in entry_controller.py: %s",
                            str(e),
                        )
                        raise HTTPException(status_code=500, detail=str(e))

                async def extract_url_content() -> Conversation:
                    conversation: Conversation = await service.extract_url_content(
                        url=input.url
                    )
                    return conversation

                entry_id_task = asyncio.create_task(post())
                conversation_task = asyncio.create_task(extract_url_content())

                # Defensively validate task_str is part of enum value (even though we still have to send it as a string through the API call)
                for task_str in input.tasks:
                    if task_str not in Task._value2member_map_:
                        raise HTTPException(
                            status_code=400, detail=f"Invalid task: {task_str}"
                        )

                conversation: Conversation = await conversation_task
                jsonified_conversation: dict[str, str] = conversation.jsonify()

                inference_input = InferenceInput(
                    conversation=conversation.jsonify(), tasks=input.tasks
                )

                try:
                    result: dict[str, Any] = await service.infer(data=inference_input)
                except Exception as e:
                    log.error(
                        "Error posting infer request to BRAIN in entry_controller.py: %s",
                        str(e),
                    )
                    raise HTTPException(status_code=500, detail=str(e))

                entry_id: str = await entry_id_task

                inference_db_input = InferenceDbInput(
                    entry_id=entry_id,
                    conversation=json.dumps(jsonified_conversation),
                    summary=result.get("summary"),
                    practice=result.get("practice"),
                )

                try:
                    await self.inference_controller.post(input=inference_db_input)
                except Exception as e:
                    log.error(
                        "Error posting to inference db in entry_controller.py: %s",
                        str(e),
                    )
                    raise HTTPException(status_code=500, detail=str(e))

                return JSONResponse(status_code=200, content=result)
            except Exception as e:
                log.error("Error starting in entry_controller.py: %s", str(e))
                raise HTTPException(status_code=500, detail=str(e))


entry_controller_router = EntryController().router

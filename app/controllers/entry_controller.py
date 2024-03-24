import asyncio
from typing import List
from fastapi import APIRouter, HTTPException, Request
from app.models.enum.task import Task
from app.models.logic.conversation import Conversation
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
                async def post_entry() -> str:
                    entry_id: str = await service.post_entry(input=input, return_column="entry_id")
                    return entry_id
                
                async def extract_url_content() -> Conversation:
                    conversation: Conversation = await service.extract_url_content(url=input.url)
                    return conversation
                
                entry_id_task = asyncio.create_task(post_entry())
                conversation_task = asyncio.create_task(extract_url_content())
                
                validated_tasks: List[Task] = []
                for task_str in input.tasks:
                    if task_str in Task._value2member_map_:
                        validated_tasks.append(Task(task_str))
                    else:
                        raise HTTPException(status_code=400, detail=f"Invalid task: {task_str}")

                conversation: Conversation = await conversation_task
                print(conversation.title)
                entry_id: str = await entry_id_task   
                             
                return {"entry_id": entry_id}
            except Exception as e:
                log.error("Error: %s", str(e))
                raise HTTPException(status_code=500, detail=str(e))

entry_controller_router = EntryController().router
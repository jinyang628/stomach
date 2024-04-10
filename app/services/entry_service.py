import asyncio
import json
import logging
import os
from typing import Any, List

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import HTTPException

from app.controllers.inference_controller import InferenceController
from app.controllers.user_controller import UserController
from app.models.enum.shareGpt import ShareGpt
from app.models.enum.task import Task
from app.models.logic.conversation import Conversation
from app.models.logic.message import AssistantMessage, Message, UserMessage
from app.models.stores.entry import Entry
from app.models.types import EntryDbInput, InferenceDbInput, InferenceInput
from app.services.inference_service import InferenceService
from app.services.user_service import UserService
from app.stores.entry import EntryObjectStore

log = logging.getLogger(__name__)

load_dotenv()

BRAIN_API_URL: str = os.getenv("BRAIN_API_URL")


class EntryService:

    ###
    ### Pipeline logic
    ###
    async def start_entry_process(self, input: EntryDbInput) -> dict[str, Any]:
        try:
            conversation_task = asyncio.create_task(
                self.extract_url_content(url=input.url)
            )

            tasks: list[Task] = self.validate_tasks(tasks=input.tasks)

            jsonified_conversation: dict[str, str] = await conversation_task

            inference_input = InferenceInput(
                conversation=jsonified_conversation, tasks=input.tasks
            )

            try:
                result: dict[str, Any] = await self.infer(data=inference_input)

                # Only post to entry db/increment usage if inference is successful
                entry_id_task = asyncio.create_task(
                    self.post_entry_and_increment_usage(input=input, tasks=tasks)
                )
            except Exception as e:
                log.error(
                    "Error posting infer request to BRAIN in entry_controller.py: %s",
                    str(e),
                )
                raise HTTPException(status_code=500, detail=str(e)) from e

            entry_id: str = await entry_id_task

            inference_db_input: list[InferenceDbInput] = (
                self.prepare_inference_db_input_lst(
                    entry_id=entry_id,
                    conversation=jsonified_conversation,
                    result=result,
                )
            )

            try:
                await InferenceController(service=InferenceService()).post(
                    data=inference_db_input
                )
            except Exception as e:
                log.error(
                    "Error posting to inference db in entry_controller.py: %s",
                    str(e),
                )
                raise HTTPException(status_code=500, detail=str(e)) from e

            return result
        except Exception as e:
            log.error("Error starting in entry_controller.py: %s", str(e))
            raise HTTPException(status_code=500, detail=str(e)) from e

    async def post_entry_and_increment_usage(
        self, input: EntryDbInput, tasks: list[Task]
    ) -> str:
        try:
            increment_usage_task = asyncio.create_task(
                UserController(service=UserService()).increment_usage(
                    api_key=input.api_key, tasks=tasks
                )
            )
            post_task = asyncio.create_task(
                self.post(data=[input], return_column="entry_id")
            )

            await increment_usage_task
            entry_ids = await post_task

            return entry_ids[0]
        except Exception as e:
            log.error(
                "Error posting to entry db in entry_controller.py: %s",
                str(e),
            )
            raise HTTPException(status_code=500, detail=str(e)) from e

    ###
    ### DB logic
    ###
    async def post(self, data: list[EntryDbInput], return_column: str) -> list[Any]:
        entry_store = EntryObjectStore()
        entry_lst: list[Entry] = []
        for element in data:
            entry = Entry.local(api_key=element.api_key, url=element.url)
            entry_lst.append(entry)
        identifier_lst: list[Any] = entry_store.insert(
            entries=entry_lst, return_column=return_column
        )

        return identifier_lst

    ###
    ### API logic
    ###
    async def infer(self, data: InferenceInput) -> dict[str, Any]:
        """Sends a POST request to the Brain for inference and
        returns a dictionary containing the results of the respective
        tasks chosen. If the request fails, an HTTPException is raised.

        Args:
            entry (dict[str, str]): The entry to be sent for inference

        Raises:
            HTTPException: If inference fails
        """

        try:
            if not BRAIN_API_URL:
                raise ValueError("BRAIN_API_URL is not set in .env file.")
            url: str = f"{BRAIN_API_URL}/inference"

            data_dict = data.model_dump()

            # Make a POST request to the Brain repo, set a generous timeout of 60 seconds
            async with httpx.AsyncClient(timeout=100.0) as client:
                response = await client.post(url, json=data_dict)
                if response.status_code != 200:
                    log.error(
                        f"Inference API call failed with status code {response.status_code}, response: {response.text}"
                    )
                    raise HTTPException(
                        status_code=500, detail="Failed to complete inference"
                    )
                return response.json()
        except httpx.RequestError as req_error:
            log.error(f"Request error during inference call: {req_error}")
            log.error(
                f"Request details: URL: {req_error.request.url}, Method: {req_error.request.method}"
            )
            raise HTTPException(status_code=500, detail=str(req_error)) from req_error
        except json.JSONDecodeError as json_error:
            log.error(f"JSON decoding error: {json_error}")
            raise HTTPException(
                status_code=500, detail="Invalid JSON response"
            ) from json_error
        except Exception as e:
            log.error(f"Unexpected error in infer: {e}")
            raise HTTPException(status_code=500, detail=str(e)) from e

    ###
    ### Business logic
    ###
    def validate_tasks(self, tasks: list[str]) -> list[Task]:
        """Validates task_str is part of enum value

        Args:
            tasks (list[str]): The values of the tasks which are sent from Fingers

        Raises:
            HTTPException: If the task_str is not part of the enum value
        """
        converted_tasks: list[Task] = []
        for task_str in tasks:
            if task_str not in Task._value2member_map_:
                raise HTTPException(status_code=400, detail=f"Invalid task: {task_str}")
            converted_tasks.append(Task(task_str))
        return converted_tasks

    async def extract_url_content(self, url: str) -> dict[str, str]:
        """Extracts the title and conversation messages from the ShareGPT url provided.

        Args:
            url (str): The ShareGPT url to extract content from.

        Raises:
            ValueError: If the expected tags are not found in the HMTL content
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})

        if not script_tag:
            raise ValueError("No script_tag found in the HTML content from url")

        try:
            json_data: dict[str, any] = json.loads(script_tag.string)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON in script_tag") from e

        props: dict[str, any] = json_data.get("props")
        if not props:
            raise ValueError("No props found in json_data")

        page_props: dict[str, any] = props.get("pageProps")
        if not page_props:
            raise ValueError("No pageProps found in props")

        server_response: dict[str, any] = page_props.get("serverResponse")
        if not server_response:
            raise ValueError("No serverResponse found in pageProps")

        data: dict[str, any] = server_response.get("data")
        if not data:
            raise ValueError("No data found in serverResponse")

        title: str = data.get("title")
        if not title:
            raise ValueError("No title found in data")

        linear_conversation: List[dict[str, str]] = data.get("linear_conversation")
        if not linear_conversation:
            raise ValueError("No linear_conversation found in data")

        conversation: Conversation = None
        curr_message: Message = None
        for container in linear_conversation:

            message: dict[str, any] = container.get("message")
            # This is not an error as the message can be empty
            if not message:
                continue

            content: dict[str, any] = message.get("content")
            if not content:
                raise ValueError("No content found in message")

            desired_content: str = ""
            if content.get("content_type") == "text":
                parts: list[str] = content.get("parts")
                if not parts:
                    raise ValueError(
                        "No parts found in content when content_type is text"
                    )
                if len(parts) == 0:
                    raise ValueError("Empty parts found in content")
                # TODO: IS THIS ALWAYS TRUE?
                desired_content = parts[0]
            elif content.get("content_type") == "code":
                # Code messages are what ChatGPT runs on its own server, not important for the conversation
                continue
            elif content.get("content_type") == "execution_output":
                # Execution Output messages are what ChatGPT runs on its own server, not important for the conversation
                continue
            else:
                raise ValueError(
                    "Unforseen content_type found in content. Please review the extraction strategy."
                )

            author: dict[str, any] = message.get("author")
            if not author:
                raise ValueError("No author found in message")

            role: str = author.get("role")
            if not role:
                raise ValueError("No role found in author")
            if role == "system":
                # For now, system messages are not relevant for ShareGPT conversations
                continue

            try:
                role_enum: ShareGpt = ShareGpt(role)
            except ValueError as e:
                raise ValueError("Invalid role found in author") from e

            message: Message = None
            if role_enum == ShareGpt.USER:
                message = UserMessage(
                    content=desired_content,
                    prev_message=curr_message,
                    next_message=None,
                )
            elif role_enum == ShareGpt.ASSISTANT:
                message = AssistantMessage(
                    content=desired_content,
                    prev_message=curr_message,
                    next_message=None,
                )

            if curr_message:
                curr_message.next_message = message
                message.prev_message = curr_message
            else:
                # Keep track of the first message in the Conversation class
                conversation = Conversation(title=title, curr_message=message)
            curr_message = message

        # Uncomment this to see the prettified conversation
        # pretty_json: str = json.dumps(conversation.jsonify(), indent=4)
        # print(pretty_json)

        return conversation.jsonify()

    def prepare_inference_db_input_lst(
        self, entry_id: str, conversation: dict[str, str], result: dict[str, Any]
    ) -> list[InferenceDbInput]:
        """Prepares the input to be stored in the inference table."""
        practice_lst: list[dict[str, Any]] = result.get("practice")
        if practice_lst:
            practice_length: int = len(practice_lst)
            inference_db_input_lst: list[InferenceDbInput] = []
            for i in range(practice_length):
                inference_db_input_lst.append(
                    InferenceDbInput(
                        entry_id=entry_id,
                        conversation=json.dumps(conversation),
                        summary=json.dumps(result.get("summary")),
                        question=json.dumps(result.get("practice")[i].get("question")),
                        answer=json.dumps(result.get("practice")[i].get("answer")),
                    )
                )
            return inference_db_input_lst
        return [
            InferenceDbInput(
                entry_id=entry_id,
                conversation=json.dumps(conversation),
                summary=json.dumps(result.get("summary")),
                question=None,
                answer=None,
            )
        ]

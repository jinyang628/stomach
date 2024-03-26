import json
import logging
import os
from typing import Any, List

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import HTTPException

from app.models.enum.shareGpt import ShareGpt
from app.models.enum.task import Task
from app.models.logic.conversation import Conversation
from app.models.logic.message import AssistantMessage, Message, UserMessage
from app.models.stores.entry import Entry
from app.models.types import EntryDbInput, InferenceInput
from app.stores.entry import EntryObjectStore

log = logging.getLogger(__name__)

load_dotenv()

BRAIN_API_URL: str = os.getenv("BRAIN_API_URL")


class EntryService:

    ###
    ### DB logic
    ###
    async def post(self, input: list[EntryDbInput], return_column: str) -> list[Any]:
        store = EntryObjectStore()
        entry_lst: list[Entry] = []
        for element in input:
            entry = Entry.local(api_key=element.api_key, url=element.url)
            entry_lst.append(entry)
        identifier_lst: list[Any] = store.insert(
            entries=entry_lst, return_column=return_column
        )
        return identifier_lst

    ###
    ### API logic
    ###
    async def infer(self, data: InferenceInput) -> dict[str, Any]:
        """Sends a POST request to the Brain for inference and returns a dictionary containing the results of the respective tasks chosen. If the request fails, an HTTPException is raised.

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

            # Make a POST request to the Brain repo, set a generous timeout of 20 seconds
            async with httpx.AsyncClient(timeout=20.0) as client:
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
            raise HTTPException(status_code=500, detail=str(req_error))
        except json.JSONDecodeError as json_error:
            log.error(f"JSON decoding error: {json_error}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except Exception as e:
            log.error(f"Unexpected error in infer: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    ###
    ### Business logic
    ###

    def validate_tasks(self, tasks: list[str]) -> None:
        """Defensively validates task_str is part of enum value (even though we still have to send it as a string through the API call)

        Args:
            tasks (list[str]): The values of the tasks which are sent from Fingers

        Raises:
            HTTPException: If the task_str is not part of the enum value
        """
        for task_str in tasks:
            if task_str not in Task._value2member_map_:
                raise HTTPException(status_code=400, detail=f"Invalid task: {task_str}")

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
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in script_tag")

        props: dict[str, any] = json_data.get("props")
        if not props:
            raise ValueError("No props found in json_data")

        pageProps: dict[str, any] = props.get("pageProps")
        if not pageProps:
            raise ValueError("No pageProps found in props")

        serverResponse: dict[str, any] = pageProps.get("serverResponse")
        if not serverResponse:
            raise ValueError("No serverResponse found in pageProps")

        data: dict[str, any] = serverResponse.get("data")
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

            parts: list[str] = content.get("parts")
            if not parts:
                raise ValueError("No parts found in content")
            if len(parts) == 0:
                raise ValueError("Empty parts found in content")

            individual_response: str = parts[0]

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
            except ValueError:
                raise ValueError("Invalid role found in author")

            message: Message = None
            if role_enum == ShareGpt.USER:
                message = UserMessage(
                    content=individual_response,
                    prev_message=curr_message,
                    next_message=None,
                )
            elif role_enum == ShareGpt.ASSISTANT:
                message = AssistantMessage(
                    content=individual_response,
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

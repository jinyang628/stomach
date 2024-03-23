import json
from typing import List

from bs4 import BeautifulSoup
import requests
from app.models.enum.shareGpt import ShareGpt
from app.models.logic.conversation import Conversation
from app.models.logic.message import AssistantMessage, Message, UserMessage


# This function has to be modified when the structure of the shareGPT links changes
# For now, we only take in a single url. In the future, we will possibly take in a list of urls.
def extractUrlContent(url: str) -> Conversation:
    """Extracts the title and conversation messages from the ShareGPT url provided.

    Args:
        url (str): The ShareGPT url to extract content from.

    Raises:
        ValueError: If the expected tags are not found in the HMTL content

    Returns:
        str: _description_
    """
    # Will be a for loop in the future?
    conversation: Conversation = _extract_single_url_content(url)

    # Uncomment this to see the prettified conversation
    # pretty_json: str = json.dumps(conversation.jsonify(), indent=4)
    # print(pretty_json)

    return conversation

def _extract_single_url_content(url: str) -> Conversation:
    response = requests.get(url)
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

    return conversation

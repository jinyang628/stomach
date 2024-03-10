import json
from app.models.conversation import Conversation
from app.models.extractor import Extractor


# This function has to be modified when the structure of the shareGPT links changes
# For now, we only take in a single url. In the future, we will possibly take in a list of urls. Hence, we should abstract the logic out to the Extractor class so as to call this script only once.
def extractUrlContent(url: str):
    """Extracts the title and conversation messages from the ShareGPT url provided.

    Args:
        url (str): The ShareGPT url to extract content from.

    Raises:
        ValueError: If the expected tags are not found in the HMTL content

    Returns:
        str: _description_
    """
    extractor: Extractor = Extractor()
    # Will be a for loop in the future
    conversation: Conversation = extractor.extract_single_url_content(url)
    jsonified_conversation: dict[str, str] = conversation.jsonify()

    # Uncomment this to see the prettified conversation
    # pretty_json: str = json.dumps(jsonified_conversation, indent=4)
    # print(pretty_json)

    return jsonified_conversation

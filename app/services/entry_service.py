import uuid
from typing import List
import json
from fastapi import Request
from bson import ObjectId
from scripts.extractUrlContent import extractUrlContent
from app.models.entry import Entry
from app.models.url import UrlModel
import ast


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class EntryService:

    async def create(self, request: Request, data: UrlModel) -> dict:
        url = data.url
        jsonified_conversation: dict = extractUrlContent(url)

        # Prepare the Entry data
        dummy_user_id: str = str(uuid.uuid4())
        entry_data = {"user_id": dummy_user_id, "messages": jsonified_conversation}
        entry_model = Entry(**entry_data)

        # Since we're directly using Entry model, ensure it's serialized properly for MongoDB
        entry_dict = entry_model.dict()
        # Insert into the database (adjust this part if your db access is async)
        db = request.app.database
        new_entry = db["Entries"].insert_one(entry_dict)
        created_entry = db["Entries"].find_one({"_id": new_entry.inserted_id})
        parsed = JSONEncoder().encode(created_entry)
        unparsed = ast.literal_eval(parsed)
        return unparsed

    async def get_all(self, request: Request) -> List[Entry]:
        entries: List[dict] = []
        limit = 100  # Number of documents to fetch per query
        skip = 0  # Offset, start with 0

        # Assume collection.find() returns a cursor that can be asynchronously iterated
        # Use a loop to fetch and append documents until all documents are fetched
        while True:
            batch = (
                await request.app.database["Entries"]
                .find()
                .skip(skip)
                .limit(limit)
                .to_list(length=limit)
            )
            if not batch:
                break  # Exit the loop if no more documents are returned
            entries.extend(batch)
            skip += limit  # Increase the offset for the next batch

        return entries  # Return the list of entries

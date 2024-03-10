import uuid
from typing import List
import json
from fastapi import Request, HTTPException, status
from bson import ObjectId
from scripts.extractUrlContent import extractUrlContent
from app.models.entry import Entry
from app.models.url import UrlModel

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class EntryService:

    async def create(self, request: Request, data: UrlModel) -> Entry:
        url = data.url
        jsonified_conversation: dict = extractUrlContent(url)

        # Prepare the Entry data
        dummy_user_id: str = str(uuid.uuid4())
        entry_data = {
            "user_id": dummy_user_id,
            "messages": jsonified_conversation
        }
        entry_model = Entry(**entry_data)

        # Since we're directly using Entry model, ensure it's serialized properly for MongoDB
        entry_dict = entry_model.dict()
        # Insert into the database (adjust this part if your db access is async)
        db = request.app.database
        new_entry = db["Entries"].insert_one(entry_dict)
        created_entry = db["Entries"].find_one({"_id": new_entry.inserted_id})
        parsed = JSONEncoder().encode(created_entry)
        return parsed

    async def get_all(self, request: Request) -> List[Entry]:
        entries: List[dict] = list(request.app.database["Entries"].find(limit=100))
        return entries
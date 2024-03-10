import uuid
import logging
from typing import List
from fastapi import Body, Request, HTTPException, status
from bson import ObjectId
from app.models.entry import EntryRequest, Entry

class EntryService:
    async def create_entry(self, request: Request, entryRequest: EntryRequest) -> Entry:
        # Prepare the Entry data
        dummy_user_id: str = str(uuid.uuid4())
        entry_data = {
            "user_id": dummy_user_id,
            "messages": entryRequest
        }
        entry_model = Entry(**entry_data)

        # Since we're directly using Entry model, ensure it's serialized properly for MongoDB
        entry_dict = entry_model.dict
        
        # Insert into the database (adjust this part if your db access is async)
        db = request.app.database
        new_entry = db["Entries"].insert_one(entry_dict)
        created_entry = db["Entries"].find_one({"_id": new_entry.inserted_id})
        logging.info("Successfully extracted and saved URL content: %s", created_entry)
        return created_entry

    async def list_entries(self, request: Request) -> List[Entry]:
        entries: List[dict] = list(request.app.database["Entries"].find(limit=100))
        return entries

    async def find_entry(self, entry_id: str, request: Request) -> Entry:
        entry: dict = request.app.database["Entries"].find_one({"_id": ObjectId(entry_id)})
        if entry is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entry with ID {entry_id} not found")
        return entry

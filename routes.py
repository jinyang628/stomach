from typing import List
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo.results import InsertOneResult
from bson import ObjectId

from app.db.models import Entry

router = APIRouter()

@router.post("/", response_description="Create a new entry", response_model=Entry, status_code=status.HTTP_201_CREATED)
async def create_entry(request: Request, entry: Entry = Body(...)) -> Entry:
    entry = jsonable_encoder(entry)
    new_entry: InsertOneResult = request.app.database["Entries"].insert_one(entry)
    created_entry = request.app.database["Entries"].find_one(
        {"_id": new_entry.inserted_id}
    )
    return created_entry

@router.get("/", response_description="List all entries", response_model=List[Entry], status_code=status.HTTP_200_OK)
async def list_entries(request: Request) -> List[Entry]:
    entries: List[dict] = list(request.app.database["Entries"].find(limit=100))
    return entries

@router.get("/{entry_id}", response_description="Get a single entry by id", response_model=Entry, status_code=status.HTTP_200_OK)
async def find_entry(entry_id: str, request: Request) -> Entry:
    entry: dict = request.app.database["Entries"].find_one({"_id": ObjectId(entry_id)})
    if entry is not None:
        return entry
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entry with ID {entry_id} not found")

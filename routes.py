from typing import List
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.db.models import Entry

router = APIRouter()

@router.post("/", response_description="Create a new entry", status_code=status.HTTP_201_CREATED, response_model=Entry)
def create_entry(request: Request, entry: Entry = Body(...)):
    entry = jsonable_encoder(entry)
    new_entry = request.app.database["Entries"].insert_one(entry)
    created_entry = request.app.database["Entries"].find_one(
        {"_id": new_entry.inserted_id}
    )

    return created_entry

@router.get("/", response_description="List all entries", response_model=List[Entry])
def list_entries(request: Request):
    entries = list(request.app.database["Entries"].find(limit=100))
    return entries

@router.get("/{id}", response_description="Get a single entry by id", response_model=Entry)
def find_entry(id: str, request: Request):
    if (entry := request.app.database["Entries"].find_one({"_id": id})) is not None:
        return entry
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entry with ID {id} not found")

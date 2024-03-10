from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Request
from app.services.entryService import EntryService
from app.models.entry import Entry

class EntryController:
    def __init__(self):
        self.router = APIRouter()
        self.service = EntryService()
        self.setup_routes()

    def setup_routes(self):
        router = self.router
        service = self.service

        @router.get("/", response_model=List[Entry])
        async def list_entries(request: Request):
            entries = await service.list_entries(request)
            return entries
        
        @router.get("/{entry_id}", response_model=Entry)
        async def find_entry(entry_id: str, request: Request):
            entry = await service.find_entry(entry_id, request)
            return entry
        
        @router.post("/")
        async def create_entry(entryRequest: Entry, request: Request):
            entry = await service.create_entry(request, entryRequest)
            return entry
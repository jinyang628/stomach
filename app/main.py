from fastapi import FastAPI, HTTPException
from dotenv import dotenv_values
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models.logic.conversation import Conversation
from app.models.types import _PostEntriesInput, ValidateInput
from scripts.entry import insert_entry
from scripts.extractUrlContent import extractUrlContent


config = dotenv_values(".env")

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
    
@app.post("/api/entries")
def _post_entries(input: _PostEntriesInput):
    conversation: Conversation = extractUrlContent(input.url)  
    
    
@app.get("/api/api_keys/validate/{api_key}")
def validate(input: ValidateInput):
    try:
        # TODO: Validate the API key
        return JSONResponse(
            content={"Successfully validated": input.api_key}, status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.entry_controller import entry_controller_router
from app.controllers.api_key_controller import api_key_controller_router

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

app.include_router(entry_controller_router, tags=["entries"], prefix="/api/entries")
app.include_router(api_key_controller_router, tags=["api_keys"], prefix="/api/api_keys")

    
# conversation: Conversation = extractUrlContent(url=input.url)  
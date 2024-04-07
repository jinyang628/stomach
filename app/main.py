import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.entry_controller import entry_controller_router
from app.controllers.user_controller import api_key_controller_router

# Check operating system
if os.name == "posix":
    # macOS, Linux, or Unix
    from dotenv import dotenv_values

    config = dotenv_values(".env")
else:
    # Windows or Windows WSL
    from dotenv import load_dotenv

    load_dotenv(".env")

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

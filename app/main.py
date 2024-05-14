import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.controllers.entry_controller import EntryController
from app.controllers.user_controller import UserController
from app.services.entry_service import EntryService
from app.services.user_service import UserService

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


def get_entry_controller_router():
    service = EntryService()
    return EntryController(service=service).router


def get_user_controller_router():
    service = UserService()
    return UserController(service=service).router


app.include_router(get_entry_controller_router(), tags=["entries"], prefix="/api/entry")
app.include_router(get_user_controller_router(), tags=["user"], prefix="/api/user")

@app.get("/.well-known/pki-validation/2E191BD31FBCBFE86BD88D95CA812D4E.txt")
async def serve_ssl_validation_file(filename: str):
    file_path = os.path("./2E191BD31FBCBFE86BD88D95CA812D4E.txt")
    return FileResponse(path=file_path)

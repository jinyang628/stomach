from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.entry_controller import EntryController
from app.controllers.user_controller import UserController
from app.services.entry_service import EntryService
from app.services.user_service import UserService

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allows all origins
    allow_origins=[
        "https://fingers-beta.vercel.app",
        "http://localhost:3000",  
    ],
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

from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from models import SendUrlModel
from scripts.extractUrlContent import extractUrlContent
from routes import router as entry_router
import certifi

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"], tlsCAFile=certifi.where())
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database using certifi CA bundle!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(entry_router, tags=["entries"], prefix="/entry")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/sendUrl")
def sendUrl(data: SendUrlModel):
    url: str = data.url
    extractUrlContent(url)
    return {"Successfully extracted URL": url}
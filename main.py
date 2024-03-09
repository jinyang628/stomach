from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import certifi
from models import SendUrlModel
from scripts.extractUrlContent import extractUrlContent
from routes import router as entry_router

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

# Database initialization and cleanup logic
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"], tlsCAFile=certifi.where())
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database using certifi CA bundle!")

# Close MongoDB connection on application shutdown
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


# DB route setup    
app.include_router(entry_router, tags=["entries"], prefix="/entry")

# Application routes setup
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/sendUrl")
def sendUrl(data: SendUrlModel):
    try:
        url: str = data.url
        jsonified_conversation: dict[str, str] = extractUrlContent(url)
        print(jsonified_conversation)
        return {"Successfully extracted URL": url}, 200
    except Exception as e:
        return {"Error": str(e)}, 500

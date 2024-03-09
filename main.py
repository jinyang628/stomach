from fastapi import FastAPI, APIRouter, Body, Request, HTTPException, status
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import certifi
from models import SendUrlModel
from scripts.extractUrlContent import extractUrlContent
from routes import router as entry_router
from app.db.models import Entry


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
def sendUrl(request: Request, data: SendUrlModel):  # Assuming Request can be obtained here
    try:
        url: str = data.url
        jsonified_conversation: dict[str, str] = extractUrlContent(url)
        
        # Prepare the Entry data
        entry_data = {
            "messages": jsonified_conversation
        }
        
        # Now, use the Entry model for validation
        entry_model = Entry(**entry_data)
        
        # Since we're directly using Entry model, ensure it's serialized properly for MongoDB
        entry_dict = entry_model.dict(by_alias=True)  # 'by_alias=True' to use field aliases like '_id'
        
        # Insert into the database (adjust this part if your db access is async)
        db = request.app.database
        new_entry = db["Entries"].insert_one(entry_dict)
        created_entry = db["Entries"].find_one({"_id": new_entry.inserted_id})

        return {"Successfully extracted and saved URL content": created_entry}, 200
    except Exception as e:
        return {"Error": str(e)}, 500

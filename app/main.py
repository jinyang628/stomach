from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import certifi
from app.controllers.entry_controller import entry_controller_router

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

app.include_router(entry_controller_router, tags=["entries"], prefix="/api/entries")

@app.get("/api/api_keys/validate/{api_key}")
def validate(api_key: str):
    try:
        print(api_key)
        return JSONResponse(
            content={"Successfully validated": api_key}, status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import CreateEntryModel
from scripts.extractUrlContent import extractUrlContent

app = FastAPI()

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


@app.post("/api/entries")
def sendUrl(data: CreateEntryModel):
    try:
        url: str = data.url
        jsonified_conversation: dict[str, str] = extractUrlContent(url)
        print(jsonified_conversation)
        return JSONResponse(content={"Successfully extracted URL": url}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/api_keys/validate/{api_key}")
def validate(api_key: str):
    try:
        print(api_key)
        return JSONResponse(content={"Successfully validated": api_key}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

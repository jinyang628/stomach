from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.post("/api/createEntry")
def sendUrl(data: CreateEntryModel):
    try:
        url: str = data.url
        jsonified_conversation: dict[str, str] = extractUrlContent(url)
        print(jsonified_conversation)
        return {"Successfully extracted URL": url}, 200
    except Exception as e:
        return {"Error": str(e)}, 500

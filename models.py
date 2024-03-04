from pydantic import BaseModel

class SendUrlModel(BaseModel):
    url: str

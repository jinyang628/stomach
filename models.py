from pydantic import BaseModel, ConfigDict

class SendUrlModel(BaseModel):
    # This forbids extra parameters from being added into this interface 
    model_config = ConfigDict(extra='forbid') 

    url: str 

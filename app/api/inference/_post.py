from fastapi import HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

from app.models.entry_controller.inferenceInput import InferenceInput

load_dotenv()

BRAIN_API_URL: str = os.getenv("BRAIN_API_URL")


class BrainResponse(BaseModel):
    summary: str
    code: str

async def _post(data: InferenceInput):
    """This is a function that sends a POST request to the Brain for inference. It does not return anything. If the request fails, an HTTPException is raised.

    Args:
        entry (dict[str, str]): The entry to be sent for inference

    Raises:
        HTTPException: If inference fails
    """
    
    try:
        if not BRAIN_API_URL:
            raise ValueError("BRAIN_API_URL is not set in .env file.")
        url: str = f"{BRAIN_API_URL}/inference"
        
        # Convert Pydantic model to a dictionary
        # THIS MAY NOT BE NECSSARY AFTER return type of create_entry is fixed
        data_dict = data.model_dump()
        if data_dict.get('tasks'):
            data_dict['tasks'] = [task.value for task in data_dict['tasks']]
        else:
            raise ValueError("'tasks' are required for inference. The field in InferenceInput is not supposed to be updated.")

        # Make a POST request to the Brain repo
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data_dict)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500, detail="Failed to complete inference"
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

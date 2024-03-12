from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BRAIN_API_URL: str = os.getenv("BRAIN_API_URL")


class BrainResponse(BaseModel):
    summary: str
    code: str


async def infer(entry: dict[str, str]):
    """This is a function that sends a POST request to the Brain for inference. It does not return anything. If the request fails, an HTTPException is raised.

    Args:
        entry (dict[str, str]): The entry to be sent for inference

    Raises:
        HTTPException: If inference fails
    """
    try:
        if not BRAIN_API_URL:
            raise ValueError("BRAIN_API_URL is not set in .env file.")
        url: str = f"{BRAIN_API_URL}/infer"

        # Make a POST request to the Brain repo
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=entry)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500, detail="Failed to complete inference"
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

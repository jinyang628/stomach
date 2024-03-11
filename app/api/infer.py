from pydantic import BaseModel, ValidationError
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BRAIN_API_URL: str = os.getenv("BRAIN_API_URL")


class BrainResponse(BaseModel):
    summary: str
    code: str


async def infer(entry: dict[str, str]) -> dict[str, str]:
    try:
        if not BRAIN_API_URL:
            raise ValueError("BRAIN_API_URL is not set in .env file.")
        url: str = f"{BRAIN_API_URL}/infer"

        # Make a POST request to the ML repo
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=entry)

            if response.status_code == 200:
                # Extract the data part from the response
                response_data: dict[str, str] = response.json().get("data")
                try:
                    parsed_response = BrainResponse.model_validate(response_data)
                except ValidationError as e:
                    return {"Error": "Response validation failed"}, 500
                return parsed_response.model_dump()
            else:
                return {
                    "Error": "Failed to communicate with Brain"
                }, response.status_code
    except Exception as e:
        return {"Error": str(e)}, 500

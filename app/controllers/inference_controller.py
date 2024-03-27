import logging

from fastapi import APIRouter, HTTPException

from app.models.types import InferenceDbInput
from app.services.inference_service import InferenceService

log = logging.getLogger(__name__)

router = APIRouter()


class InferenceController:
    def __init__(self):
        self.router = APIRouter()
        self.service = InferenceService()

    async def post(self, data: InferenceDbInput) -> str:
        try:
            id: str = await self.service.post(data=[data], return_column="id")
            return id
        except Exception as e:
            log.error(
                f"Error posting to inference db from inference_controller.py: {e}"
            )
            raise HTTPException(status_code=500, detail="Internal server error") from e

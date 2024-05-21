import logging
from fastapi import APIRouter
from app.services.inference_service import InferenceService

log = logging.getLogger(__name__)

router = APIRouter()


class InferenceController:
    def __init__(self, service: InferenceService):
        self.router = APIRouter()
        self.service = service
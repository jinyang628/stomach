from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.api_key_service import ApiKeyService 
import logging

log = logging.getLogger(__name__)

router = APIRouter()

class ApiKeyController:
    def __init__(self):
        self.router = APIRouter()
        self.service = ApiKeyService()
        self.setup_routes()
    
    def setup_routes(self):
        router = self.router
        service = self.service
        
        @router.get("/validate/{api_key}")    
        async def validate(api_key: str):
            try:
                isValidApiKey: bool = service.validate_api_key(api_key)
                if not isValidApiKey:
                    return JSONResponse(status_code=401, content={"message": "Invalid API Key"})
                return JSONResponse(status_code=200, content={"message": "API Key successfully validated"})
            except Exception as e:
                log.error("Error: %s", str(e))
                return JSONResponse(status_code=500, content={"Error": str(e)})

api_key_controller_router = ApiKeyController().router  
import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.models.enum.task import Task
from app.services.user_service import UserService

log = logging.getLogger(__name__)

router = APIRouter()


class UserController:
    def __init__(self):
        self.router = APIRouter()
        self.service = UserService()
        self.setup_routes()

    def setup_routes(self):
        router = self.router
        service = self.service

        @router.get("/validate/{api_key}")
        async def validate(api_key: str):
            try:
                is_valid_api_key: bool = service.validate_api_key(api_key=api_key)
                if not is_valid_api_key:
                    return JSONResponse(
                        status_code=401, content={"message": "Invalid API Key"}
                    )
                return JSONResponse(
                    status_code=200,
                    content={"message": "API Key successfully validated"},
                )
            except Exception as e:
                log.error(f"Error: {str(e)} in UserController#setup_routes#validate")
                return JSONResponse(status_code=500, content={"Error": str(e)})

    def increment_usage(self, api_key: str, tasks: list[Task]) -> bool:
        try:
            is_usage_incremented: bool = self.service.increment_usage(
                api_key=api_key, tasks=tasks
            )
            if not is_usage_incremented:
                log.error(f"Error incrementing usage for api_key: {api_key}")
                raise HTTPException(status_code=500, detail=str(e)) from e
            return is_usage_incremented
        except Exception as e:
            log.error(f"Error: {str(e)} in UserController#increment_usage")
            raise HTTPException(status_code=500, detail=str(e)) from e


api_key_controller_router = UserController().router

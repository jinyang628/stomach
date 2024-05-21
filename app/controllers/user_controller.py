import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.exceptions.exception import DatabaseError
from app.services.user_service import UserService

log = logging.getLogger(__name__)

router = APIRouter()


class UserController:
    def __init__(self, service: UserService):
        self.router = APIRouter()
        self.service = service
        self.setup_routes()

    def setup_routes(self):
        router = self.router

        @router.get("/validate/{api_key}")
        async def validate(api_key: str) -> JSONResponse:
            """Validates the API Key.

            Args:
                api_key (str): The API Key to be validated.

            Returns:
                JSONResponse: The response indicating whether the API Key is valid or not that should be passed back to Fingers.
            """
            try:
                is_valid_api_key: bool = self.service.validate_api_key(api_key=api_key)
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

    async def increment_usage(self, api_key: str, token_sum: int):
        """Increments the usage for the API Key in the user table.

        Args:
            api_key (str): The API Key for which the usage is to be incremented.
            token_sum (int): The number of tokens to increment the usage by.

        Returns:
            bool: A boolean indicating whether the usage was successfully incremented or not.
        """
        try:
            self.service.increment_usage(api_key=api_key, token_sum=token_sum)
        except DatabaseError as e:
            log.error(f"Database error: {str(e)} in UserController#increment_usage")
            raise e
        except Exception as e:
            log.error(f"Unexpected error while incrementing_usage: {str(e)}")
            raise e

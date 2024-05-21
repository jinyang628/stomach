import logging

from app.connectors.orm import Orm
from app.exceptions.exception import DatabaseError
from app.models.stores.user import User, UserORM
from dotenv import find_dotenv, load_dotenv
import os
log = logging.getLogger(__name__)

load_dotenv(find_dotenv(filename=".env"))
TURSO_DB_URL = os.environ.get("TURSO_DB_URL")
TURSO_DB_AUTH_TOKEN = os.environ.get("TURSO_DB_AUTH_TOKEN")

USAGE_LIMIT: int = 400_000 # Adjust this accordingly in production

class UserService:

    def is_within_limit(self, api_key: str) -> bool:
        """Valides if the user is within the limit

        Args:
            api_key (str): The API key of the user

        Returns:
            bool: _description_
        """
        orm = Orm(url=TURSO_DB_URL, auth_token=TURSO_DB_AUTH_TOKEN)
        try:
            users: list[User] = orm.get(model=UserORM, filters={"api_key": api_key})
            if len(users) > 1:
                raise ValueError(f"Multiple users found for api_key: {api_key}")
            if len(users) == 0:
                raise ValueError(f"No user found for api_key: {api_key}")
            return users[0].usage < USAGE_LIMIT
        except Exception as e:
            raise DatabaseError(message=str(e)) from e

    def validate_api_key(self, api_key: str) -> bool:
        """Validates the API key in the user table

        Args:
            api_key (str): The API key of the user

        Returns:
            bool: _description_
        """
        orm = Orm(url=TURSO_DB_URL, auth_token=TURSO_DB_AUTH_TOKEN)
        users: list[User] = orm.get(model=UserORM, filters={"api_key": api_key})
        if len(users) > 1:
            raise ValueError(f"Multiple users found for api_key: {api_key}")
        elif len(users) == 0:
            log.error(f"No user found for api_key: {api_key}")
            return False
        return True

    def increment_usage(self, api_key: str, token_sum: int) -> bool:
        """Increments the usage of the user in the user table

        Args:
            api_key (str): The API key of the user
            token_sum (int): The token sum to increment
        """
        if not token_sum:
            raise ValueError("Token sum cannot be empty in the API call")
        orm = Orm(url=TURSO_DB_URL, auth_token=TURSO_DB_AUTH_TOKEN)
        try:
            users: list[User] = orm.get(model=UserORM, filters={"api_key": api_key})
            if len(users) > 1:
                raise ValueError(f"Multiple users found for api_key: {api_key}")
            if len(users) == 0:
                raise ValueError(f"No user found for api_key: {api_key}")
            incremented_usage: int = users[0].usage + token_sum
            orm.update(
                model=UserORM, 
                filters={"api_key": api_key}, 
                update={"usage": incremented_usage}
            )
        except DatabaseError as e:
            log.error(f"Database error: {str(e)} in UserService#increment_usage")
            raise e
        except Exception as e:
            log.error(f"Unexpected error while incrementing_usage: {str(e)}")
            raise e

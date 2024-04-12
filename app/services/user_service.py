from app.exceptions.exception import DatabaseError
from app.stores.user import UserObjectStore
import logging

log = logging.getLogger(__name__)

class UserService:
    
    def is_within_limit(self, api_key: str) -> bool:
        """Valides if the user is within the limit

        Args:
            api_key (str): The API key of the user

        Returns:
            bool: _description_
        """
        try:
            is_within_limit: bool = UserObjectStore().is_within_limit(api_key=api_key)
            return is_within_limit
        except Exception as e:
            raise DatabaseError(message=str(e)) from e
        
        
    def validate_api_key(self, api_key: str) -> bool:
        """Validates the API key in the user table

        Args:
            api_key (str): The API key of the user

        Returns:
            bool: _description_
        """
        return UserObjectStore().validate_api_key(api_key=api_key)

    def increment_usage(self, api_key: str, token_sum: int) -> bool:
        """Increments the usage of the user in the user table

        Args:
            api_key (str): The API key of the user
            token_sum (int): The token sum to increment
        """
        if not token_sum:
            raise ValueError("Token sum cannot be empty in the API call")
        try:
            is_incremented: bool = UserObjectStore().increment_usage(
                api_key=api_key, usage_counter=token_sum
            )
            return is_incremented
        except DatabaseError as e:
            log.error(f"Database error: {str(e)} in UserService#increment_usage")
            raise e
        except Exception as e:
            log.error(f"Unexpected error while incrementing_usage: {str(e)}")
            raise e
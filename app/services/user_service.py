from app.models.enum.task import Task
from app.stores.user import UserObjectStore


class UserService:
    def validate_api_key(self, api_key: str) -> bool:
        """Validates the API key in the user table

        Args:
            api_key (str): _description_

        Returns:
            bool: _description_
        """
        store = UserObjectStore()
        return store.validate_api_key(api_key=api_key)

    def increment_usage(self, api_key: str, token_sum: int) -> bool:
        """Increments the usage of the user in the user table

        Args:
            api_key (str): _description_
            tasks (list[str]): _description_
        """
        if not token_sum:
            raise ValueError("Token sum cannot be empty in the API call")

        return UserObjectStore().increment_usage(api_key=api_key, usage_counter=token_sum)

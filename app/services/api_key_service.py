from app.stores.user import UserObjectStore


class ApiKeyService:
    def validate(self, api_key: str) -> bool:
        """Validates the API key in the user table

        Args:
            api_key (str): _description_

        Returns:
            bool: _description_
        """
        store = UserObjectStore()
        is_valid: bool = store.validate_api_key(api_key=api_key)
        return is_valid

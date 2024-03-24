from app.stores.user import UserObjectStore

class ApiKeyService:
    def validate(self, api_key: str) -> bool:
        store = UserObjectStore()
        is_valid: bool = store.validate_api_key(api_key=api_key)
        return is_valid
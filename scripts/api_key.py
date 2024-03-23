from app.stores.user import UserObjectStore

def validate_api_key(api_key: str) -> bool:
    store = UserObjectStore()
    return store.validate_api_key(api_key=api_key)
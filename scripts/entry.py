# from typing import List
# from app.models.stores.entry import Entry
# from app.stores.entry import EntryObjectStore


# def insert_with_entry_id_return(api_key: str, url: str) -> List[str]:
#     store = EntryObjectStore()
#     entry = Entry.local(api_key=api_key, url=url)
#     return store.insert_with_entry_id_return(entries=[entry])
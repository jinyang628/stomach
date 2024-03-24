# from app.models.stores.entry import Entry
# from app.stores.entry import EntryObjectStore


# class EntryService:
#     def perform_inference(self, input: _PostEntriesInput, return_column: str) -> str:
#         store = EntryObjectStore()
#         entry = Entry.local(api_key=input.api_key, url=input.url)
#         entry_id = store.insert(entries=[entry], return_column=return_column)
#         return entry_id
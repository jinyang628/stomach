# # Use this script to do testing/one time operations on the database

# from app.stores.base.object import ObjectStore
# import logging

# log = logging.getLogger(__name__)

# def main():
#     obj_store = ObjectStore("inference")
#     obj_store.create_table("inference", {
#         "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
#         "version": "INTEGER",
#         "entry_id": "TEXT",
#         "conversation": "JSON",
#         "summary": "TEXT",
#         "exercise": "TEXT",
#     })


# if __name__ == "__main__":
#     main()

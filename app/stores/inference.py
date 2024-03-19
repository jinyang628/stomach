import os
import logging
from app.stores.base.object import ObjectStore

log = logging.getLogger(__name__)


class InferenceObjectStore:
    _store: ObjectStore = None
    
    def __init__(self):
        self._store = ObjectStore(
            table_name=os.environ.get("TURSO_DB_INFERENCE_TABLE_NAME"),
        )
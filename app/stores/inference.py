import os
import logging
from typing import List
from app.models.stores.inference import Inference
from app.stores.base.object import ObjectStore

log = logging.getLogger(__name__)


class InferenceObjectStore:
    _store: ObjectStore = None
    
    def __init__(self):
        self._store = ObjectStore(
            table_name=os.environ.get("TURSO_DB_INFERENCE_TABLE_NAME"),
        )
        
    def insert(
        self,
        inferences: List[Inference]
    ) -> List[int]:
        return self._store.insert(objs=[inference.model_dump() for inference in inferences])
    
    def get(
        self,
        ids: List[int],
    ) -> List[Inference]:
        _dicts = self._store.get(ids=ids)
        return [Inference.remote(**_dict) for _dict in _dicts]
    
    def update(
        self,
        inferences: List[Inference]
    ) -> bool:
        return self._store.update(objs=[inference.model_dump() for inference in inferences])
    
    def delete(
        self,
        ids: List[int]
    ) -> bool:
        return self._store.delete(ids=ids)
      
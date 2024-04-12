import logging
import sqlite3

from app.exceptions.exception import DatabaseError
from app.models.stores.inference import Inference
from app.models.types import InferenceDbInput
from app.stores.inference import InferenceObjectStore

log = logging.getLogger(__name__)

class InferenceService:
    async def post(self, data: list[InferenceDbInput], return_column: str) -> str:
        store = InferenceObjectStore()
        inference_lst: list[Inference] = []
        for element in data:
            inference = Inference.local(
                entry_id=element.entry_id,
                conversation=element.conversation,
                summary=element.summary,
                question=element.question,
                answer=element.answer,
            )
            inference_lst.append(inference)
        try:
            identifier: str = store.insert(
                inferences=inference_lst, return_column=return_column
            )
            return identifier
        except sqlite3.IntegrityError as e:
            # Unlikely scenario but possible. LLM generates the exact SAME values for all the columns
            if "UNIQUE constraint failed" in str(e):
                log.error(
                    f"EXACT same entry exists in inference table already. Do not insert this entry"
                )
            else:
                raise ValueError(f"Error inserting inferences: {str(e)}") from e
        except DatabaseError as e:
            log.error(f"Database error: {str(e)} in InferenceService#post")
            raise e
        except Exception as e:
            log.error(f"Unexpected error while inserting inferences: {str(e)}")
            raise e

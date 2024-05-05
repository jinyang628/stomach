import logging
import sqlite3
from typing import Any

from app.exceptions.exception import DatabaseError
from app.models.stores.inference import Inference
from app.models.types import InferenceDbInput
from app.stores.inference import InferenceObjectStore

log = logging.getLogger(__name__)


class InferenceService:
    async def post(self, data: list[InferenceDbInput], return_column: str) -> list[Any]:
        """Insert a list of inference data points into the inference table.

        Args:
            data (list[InferenceDbInput]): The list of inference data points to be inserted.
            return_column (str): The column value to return after insertion.
        Returns:
            list[Any]: The list of the identifiers of the successfully inserted the data points (can be modified to return other column values).
        """
        store = InferenceObjectStore()
        inference_lst: list[Inference] = []
        for element in data:
            inference = Inference.local(
                entry_id=element.entry_id,
                conversation=element.conversation,
                summary=element.summary,
                summary_chunk=element.summary_chunk,
                question=element.question,
                half_completed_code=element.half_completed_code,
                fully_completed_code=element.fully_completed_code,
                language=element.language,
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

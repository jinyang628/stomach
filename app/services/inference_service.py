import logging
import sqlite3
from dotenv import find_dotenv, load_dotenv
import os

from app.connectors.orm import Orm
from app.exceptions.exception import DatabaseError
from app.models.stores.inference import Inference
from app.models.types import InferenceDbInput
log = logging.getLogger(__name__)

load_dotenv(find_dotenv(filename=".env"))
TURSO_DB_URL = os.environ.get("TURSO_DB_URL")
TURSO_DB_AUTH_TOKEN = os.environ.get("TURSO_DB_AUTH_TOKEN")

class InferenceService:
    async def post(self, data: list[InferenceDbInput]):
        """Insert a list of inference data points into the inference table.

        Args:
            data (list[InferenceDbInput]): The list of inference data points to be inserted.
        """
        orm = Orm(url=TURSO_DB_URL, auth_token=TURSO_DB_AUTH_TOKEN)
        inference_lst: list[Inference] = []
        for element in data:
            inference = Inference.local(
                entry_id=element.entry_id,
                conversation=element.conversation,
                result=element.result,
            )
            inference_lst.append(inference)
        try:
            orm.insert(models=inference_lst)
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

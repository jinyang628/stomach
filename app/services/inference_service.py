from app.models.stores.inference import Inference
from app.models.types import InferenceDbInput
from app.stores.inference import InferenceObjectStore


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
                answer=element.answer
            )
            inference_lst.append(inference)
        identifier: str = store.insert(
            inferences=inference_lst, return_column=return_column
        )
        return identifier

from unittest.mock import Mock, patch

import pytest

from app.models.stores.inference import Inference
from app.models.types import InferenceDbInput
from app.services.inference_service import InferenceService
from app.stores.inference import InferenceObjectStore


@pytest.mark.asyncio
async def test_post_success():
    # Mock dependencies
    mock_inference_store = Mock(InferenceObjectStore)
    mock_inference_store.insert.return_value = "unique_id"

    mock_inference = Mock(Inference)

    input_data = [
        InferenceDbInput(
            entry_id="123",
            conversation="Test conversation",
            summary="Test summary",
            practice="Test practice",
        )
    ]

    with patch(
        "app.services.inference_service.InferenceObjectStore",
        return_value=mock_inference_store,
    ):
        with patch(
            "app.services.inference_service.Inference.local",
            return_value=mock_inference,
        ):
            service = InferenceService()
            identifier = await service.post(input=input_data, return_column="id")
            assert identifier == "unique_id"


@pytest.mark.asyncio
async def test_post_failure():
    # Mock dependencies to simulate an error
    mock_inference_store = Mock(InferenceObjectStore)
    mock_inference_store.insert.side_effect = Exception("DB Insert Failed")

    mock_inference = Mock(Inference)

    input_data = [
        InferenceDbInput(
            entry_id="123",
            conversation="Test conversation",
            summary="Test summary",
            practice="Test practice",
        )
    ]

    with patch(
        "app.services.inference_service.InferenceObjectStore",
        return_value=mock_inference_store,
    ):
        with patch(
            "app.services.inference_service.Inference.local",
            return_value=mock_inference,
        ):
            service = InferenceService()
            with pytest.raises(Exception) as excinfo:
                await service.post(input=input_data, return_column="id")
            assert str(excinfo.value) == "DB Insert Failed"

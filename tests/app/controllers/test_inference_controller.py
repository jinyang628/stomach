from fastapi import HTTPException
import pytest
from unittest.mock import AsyncMock
from app.controllers.inference_controller import InferenceController
from app.models.types import InferenceDbInput
from app.services.inference_service import InferenceService

@pytest.fixture
def mock_inference_service(mocker):
    mock_service = AsyncMock(spec=InferenceService)
    mocker.patch("app.controllers.inference_controller.InferenceService", return_value=mock_service)
    return mock_service

@pytest.fixture
def mock_inference_controller(mock_inference_service):
    return InferenceController(service=mock_inference_service)


@pytest.mark.asyncio
async def test_post_success(mock_inference_controller, mock_inference_service):
    # Mock return value
    mock_inference_service.post.return_value = "12345"

    # Prepare input data
    input_data = [InferenceDbInput(
        entry_id="shawn",
        conversation="Should I use the upper case or lower case for the type hint",
        summary="You should use lower case",
        question="test question",
        answer="test answer",
    )]

    # Perform test
    response = await mock_inference_controller.post(data=input_data)
    assert response == "12345"

@pytest.mark.asyncio
async def test_post_error(mock_inference_controller, mock_inference_service):
    # Mock service to raise an exception
    mock_inference_service.post.side_effect = Exception("Test error")

    # Prepare input data
    input_data = [InferenceDbInput(
        entry_id="shawn",
        conversation="Should I use the upper case or lower case for the type hint",
        summary="You should use lower case",
        question="test question",
        answer="test answer",
    )]

    # Perform test with expectation of HTTPException
    with pytest.raises(HTTPException) as excinfo:
        await mock_inference_controller.post(data=input_data)

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Internal server error"

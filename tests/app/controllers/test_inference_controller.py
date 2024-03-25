import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from app.controllers.inference_controller import InferenceController
from app.models.types import InferenceDbInput

@pytest.mark.asyncio
async def test_post_success():
    # Mock the InferenceService
    mock_service = AsyncMock()
    mock_service.post.return_value = '12345'
    input_data = InferenceDbInput(entry_id="shawn", conversation="Should i use the upper case or lower case for the type hint", summary="You should use lower case", practice=None) 

    with patch('app.controllers.inference_controller.InferenceService', return_value=mock_service):
        controller = InferenceController()
        response = await controller.post(input_data)
        assert response == '12345'

@pytest.mark.asyncio
async def test_post_error():
    # Mock the InferenceService to raise an exception
    mock_service = AsyncMock()
    mock_service.post.side_effect = Exception('Test error')
    input_data = InferenceDbInput(entry_id="shawn", conversation="Should i use the upper case or lower case for the type hint", summary="You should use lower case", practice=None) 

    with patch('app.controllers.inference_controller.InferenceService', return_value=mock_service):
        controller = InferenceController()
        with pytest.raises(HTTPException) as excinfo:
            await controller.post(input_data)
        
        assert excinfo.value.status_code == 500
        assert excinfo.value.detail == "Internal server error"

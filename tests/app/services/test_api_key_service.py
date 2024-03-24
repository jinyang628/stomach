import pytest
from unittest.mock import patch
from app.services.api_key_service import ApiKeyService

@pytest.fixture
def mock_store():
    with patch('app.services.api_key_service.UserObjectStore') as mock:
        yield mock

@pytest.fixture
def api_key_input():
    return "test_api_key"

def test_validate(mock_store, api_key_input):
    expected_is_valid: bool = True
    mock_store.return_value.validate_api_key.return_value = expected_is_valid
    is_valid: bool = ApiKeyService().validate(api_key=api_key_input) 
    assert is_valid == expected_is_valid
    
    mock_store.return_value.validate_api_key.assert_called_once()
    args, kwargs = mock_store.return_value.validate_api_key.call_args

    assert 'api_key' in kwargs
    api_key: str = kwargs['api_key']
    assert api_key == api_key_input 

def test_validate_handles_exceptions(mock_store, api_key_input):
    mock_store.return_value.validate_api_key.side_effect = Exception("Test Exception")
    
    with pytest.raises(Exception) as excinfo:
        ApiKeyService().validate(api_key_input)
    
    assert "Test Exception" in str(excinfo.value)

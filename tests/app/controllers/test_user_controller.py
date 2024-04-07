from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_validate_api_key_successful():
    with patch("app.services.user_service.UserService.validate_api_key") as mock_validate:
        mock_validate.return_value = True
        response = client.get("/api/api_keys/validate/test_api_key")
        assert response.status_code == 200
        assert response.json() == {"message": "API Key successfully validated"}


def test_validate_api_key_unsuccessful():
    with patch("app.services.user_service.UserService.validate_api_key") as mock_validate:
        mock_validate.return_value = False
        response = client.get("/api/api_keys/validate/invalid_api_key")
        assert response.status_code == 401
        assert response.json() == {"message": "Invalid API Key"}


def test_validate_api_key_exception():
    with patch("app.services.user_service.UserService.validate_api_key") as mock_validate:
        mock_validate.side_effect = Exception("Test Exception")
        response = client.get("/api/api_keys/validate/api_key")
        assert response.status_code == 500
        assert response.json() == {"Error": "Test Exception"}

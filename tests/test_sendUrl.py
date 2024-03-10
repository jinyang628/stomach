import pytest
from app.models.sendUrl import CreateEntryModel
from pydantic import ValidationError

SEND_URL_MODEL_VALID_DATA = [
    ("https://example.com", "https://example.com"),
]


@pytest.mark.parametrize("input_url, expected", SEND_URL_MODEL_VALID_DATA)
def test_send_url_model_valid(input_url, expected):
    data = {"url": input_url}
    model = CreateEntryModel(**data)
    assert model.url == expected


SEND_URL_MODEL_INVALID_DATA = [
    (123),  # Integer
    ({"not": "a string"}),  # Dictionary
    ([1, 2, 3]),  # List
    (None),
]


@pytest.mark.parametrize("invalid_input", SEND_URL_MODEL_VALID_DATA)
def test_send_url_model_invalid_type(invalid_input):
    with pytest.raises((TypeError, ValueError)):
        CreateEntryModel(url=invalid_input)


def test_send_url_model_too_many_params():
    with pytest.raises(ValidationError):
        CreateEntryModel(url="https://example.com", extra_param="extra")

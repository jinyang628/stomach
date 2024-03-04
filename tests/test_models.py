import pytest
from models import SendUrlModel

@pytest.mark.parametrize("input_url, expected", [
    ("https://example.com", "https://example.com"),
    ("http://test.com", "http://test.com"),
])
def test_send_url_model_valid(input_url, expected):
    data = {"url": input_url}
    model = SendUrlModel(**data)
    assert model.url == expected

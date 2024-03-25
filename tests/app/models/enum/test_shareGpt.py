import pytest

from app.models.enum.shareGpt import ShareGpt


def test_enum_contains_correct_members():
    assert ShareGpt.USER
    assert ShareGpt.ASSISTANT


ENUM_VALUE_TEST_DATA = [(ShareGpt.USER, "user"), (ShareGpt.ASSISTANT, "assistant")]


@pytest.mark.parametrize("enum_member, expected_value", ENUM_VALUE_TEST_DATA)
def test_enum_values(enum_member, expected_value):
    assert enum_member.value == expected_value

import pytest

from app.models.enum.task import Task


def test_enum_contains_correct_members():
    assert Task.SUMMARISE
    assert Task.PRACTICE


ENUM_VALUE_TEST_DATA = [(Task.SUMMARISE, "summarise"), (Task.PRACTICE, "practice")]


@pytest.mark.parametrize("enum_member, expected_value", ENUM_VALUE_TEST_DATA)
def test_enum_values(enum_member, expected_value):
    assert enum_member.value == expected_value
    
GET_USAGE_VALUE_TEST_DATA = [
    (Task.SUMMARISE, 1),
    (Task.PRACTICE, 5),
]

@pytest.mark.parametrize("enum_member, expected_value", GET_USAGE_VALUE_TEST_DATA)
def test_get_usage_value(enum_member, expected_value):
    assert enum_member.get_usage_value() == expected_value

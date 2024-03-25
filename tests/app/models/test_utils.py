from datetime import datetime
from typing import List

import pytest

from app.models.utils import sql_value_to_typed_value

SQL_VALUE_TO_TYPED_VALUE_VALID_DATA = [
    ({"name": "John"}, "name", str, "John"),
    ({"age": "30"}, "age", int, 30),
    (
        {"timestamp": "2022-03-01 15:00:00"},
        "timestamp",
        datetime,
        datetime(2022, 3, 1, 15, 0),
    ),
    ({"flag": "True"}, "flag", bool, True),
    ({"score": "9.5"}, "score", float, 9.5),
    ({"list_str": "apple,banana"}, "list_str", List[str], ["apple", "banana"]),
    ({"list_int": "1,2,3"}, "list_int", List[int], [1, 2, 3]),
    ({"some_key": "some_value"}, "nonexistent_key", str, None),  # Key not in dict
]


@pytest.mark.parametrize(
    "input_dict, key, expected_type, expected_output",
    SQL_VALUE_TO_TYPED_VALUE_VALID_DATA,
)
def test_sql_value_to_typed_value(input_dict, key, expected_type, expected_output):
    try:
        result = sql_value_to_typed_value(input_dict, key, expected_type)
        assert result == expected_output
    except Exception as e:
        assert isinstance(e, ValueError)


SQL_VALUE_TO_TYPED_VALUE_INVALID_DATA = [
    (
        {"key_containing_invalid_value": {"shawn": "kok"}},
        "key_containing_invalid_value",
        dict,
        None,
    ),
    ({"some_key": "some_value"}, "some_key", int, None),
]


@pytest.mark.parametrize(
    "input_dict, key, expected_type, expected_output",
    SQL_VALUE_TO_TYPED_VALUE_INVALID_DATA,
)
def test_sql_value_to_typed_value_invalid_data(
    input_dict, key, expected_type, expected_output
):
    with pytest.raises(ValueError):
        sql_value_to_typed_value(input_dict, key, expected_type)

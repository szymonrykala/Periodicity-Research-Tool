import pytest
from numpy import array, ndarray

from sprt.utils import bytes_to_str, validate_digit


@pytest.mark.parametrize(
    "data,expected",
    [
        ("test string", "test string"),
        ([48, 49, 50, 51, 52, 53, 54], "0123456"),
        (array([48, 49, 50, 51, 52, 53, 54]), "0123456"),
    ],
)
def test_bytes_to_str_parsing(data: list | ndarray | str, expected: str):
    out_str = bytes_to_str(data)
    assert isinstance(out_str, str)
    assert out_str == expected


@pytest.mark.parametrize(
    "value,result",
    [
        ("1", True),
        (".", True),
        ("1,1", False),
        ("1df", False),
        ("df1", False),
        ("df", False),
    ],
)
def test_validate_is_digit(value, result):
    assert validate_digit(value) == result

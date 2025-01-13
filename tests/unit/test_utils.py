import pytest
import numpy as np
from sprt.utils import bytes_to_str, validate_digit_input


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ([97, 98, 99], "abc"),
        (np.array([97, 98, 99]), "abc"),
        (b"abc", "abc"),
        ("abc", "abc"),
        ([255], str(b"\xff")),
        ([128, 129], str(b"\x80\x81")),
        ([], ""),
        (np.array([]), ""),
    ],
)
def test_bytes_to_str(input_value, expected_output):
    assert bytes_to_str(input_value) == expected_output


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ("123", True),
        ("12.3", False),
        (".", True),
        ("abc", False),
        ("12a", False),
        ("", True),
    ],
)
def test_validate_digit(input_value, expected_output):
    assert validate_digit_input(input_value) == expected_output

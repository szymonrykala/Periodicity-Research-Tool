import pytest

from sprt.algorithms.library.kmp import main


@pytest.mark.parametrize(
    "text, pattern, expected",
    [
        # Przypadki podstawowe
        ([1, 2, 3, 4, 2, 3], [2, 3], [1, 4]),
        ([1, 1, 1, 1, 1], [1, 1], [0, 1, 2, 3]),
        ([1, 2, 3, 4], [5], []),
        ([1, 2, 3], [1, 2, 3], [0]),
        ([1, 2, 3], [], []),
        ([], [1, 2], []),
        ([], [], []),
        ([1, 2, 3, 4], [4], [3]),
        # Przypadki ze stringami
        ("abcabc", "abc", [0, 3]),
        ("aaaaa", "aa", [0, 1, 2, 3]),
        ("abcd", "e", []),
        ("abc", "abc", [0]),
        ("abc", "", []),
        ("", "ab", []),
        ("", "", []),
        ("abcd", "d", [3]),
    ],
)
def test_main(text, pattern, expected):
    assert main(text=text, pattern=pattern) == expected

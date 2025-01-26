import pytest

from sprt.algorithms.library.rk import main


@pytest.mark.parametrize(
    "text, pattern, alphabet_size, prime, expected",
    [
        # Przypadki podstawowe
        ([1, 2, 3, 4, 2, 3], [2, 3], 256, 1000003, [1, 4]),
        ([1, 1, 1, 1, 1], [1, 1], 256, 1000003, [0, 1, 2, 3]),
        ([1, 2, 3, 4], [5], 256, 1000003, []),
        ([1, 2, 3], [1, 2, 3], 256, 1000003, [0]),
        ([1, 2, 3], [], 256, 1000003, []),
        ([], [1, 2], 256, 1000003, []),
        ([], [], 256, 1000003, []),
        ([1, 2, 3, 4], [4], 256, 1000003, [3]),
        # Przypadki z niestandardowym alfabetem i liczbą pierwszą
        ([1, 2, 3, 4, 2, 3], [2, 3], 10, 101, [1, 4]),
        ([1, 1, 1, 1], [1], 5, 13, [0, 1, 2, 3]),
        # Przypadki ze stringami reprezentowanymi jako kody ASCII
        ([97, 98, 99, 97, 98, 99], [97, 98, 99], 256, 1000003, [0, 3]),
        ([97, 97, 97, 97, 97], [97, 97], 256, 1000003, [0, 1, 2, 3]),
        ([97, 98, 99, 100], [101], 256, 1000003, []),
        ([97, 98, 99], [97, 98, 99], 256, 1000003, [0]),
        ([97, 98, 99], [], 256, 1000003, []),
        ([], [97, 98], 256, 1000003, []),
        ([], [], 256, 1000003, []),
        ([97, 98, 99, 100], [100], 256, 1000003, [3]),
    ],
)
def test_main(text, pattern, alphabet_size, prime, expected):
    assert main(text=text, pattern=pattern, alphabet_size=alphabet_size, prime=prime) == expected

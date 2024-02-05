import pytest
from numpy import array, ndarray

from sprt.text_generator import Generator, RandomText
from sprt.text_generator.distributions import Normal


@pytest.fixture
def generator():
    yield Generator()


__expected = array((97, 98, 99, 100, 101, 102, 103, 104, 105, 106))


@pytest.mark.parametrize(
    "charset_data, expected",
    [
        ("abcdcefghji", __expected),
        (
            "abcdcefghji".encode(),
            __expected,
        ),
        (
            tuple("abcdcefghji".encode()),
            __expected,
        ),
    ],
)
def test_generator_charset(charset_data, expected: ndarray, generator: Generator):
    assert isinstance(generator.char_set, ndarray)
    assert len(generator.char_set) > 0

    generator.char_set = charset_data
    assert generator.char_set.tolist() == expected.tolist()


@pytest.mark.parametrize("length", [200, 100, 20, 10, 5, 1])
def test_text_generation(length: int, generator):
    generator.char_set = "abcd"

    text = generator.generate(length, Normal(2, 0.1))

    assert isinstance(text, RandomText)

    assert isinstance(text.charset, ndarray)
    assert text.parsed_charset == "abcd"

    assert isinstance(text.text, ndarray)
    assert len(text.text) == length

    text.wait()
    assert isinstance(text.density_matrix, ndarray)
    assert isinstance(text.mean, float)
    assert isinstance(text.stdev, float)
    assert text.length == length

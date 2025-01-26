from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from sprt.text_generator.distributions import Normal
from sprt.text_generator.generator import Generator, RandomText


def test_generator_initialization():
    generator = Generator()
    assert isinstance(generator.char_set, np.ndarray)
    assert len(generator.char_set) > 0  # DEFAULT_CHARSET powinien być niepusty


def test_generator_char_set_setter_with_string():
    generator = Generator()
    generator.char_set = "abc"
    assert isinstance(generator.char_set, np.ndarray)
    assert len(generator.char_set) == 3
    assert sorted(generator.char_set.tolist()) == sorted([ord("a"), ord("b"), ord("c")])


def test_generator_char_set_setter_with_bytes():
    generator = Generator()
    generator.char_set = b"xyz"
    assert isinstance(generator.char_set, np.ndarray)
    assert len(generator.char_set) == 3
    assert sorted(generator.char_set.tolist()) == sorted([ord("x"), ord("y"), ord("z")])


def test_generator_char_set_setter_with_ndarray():
    generator = Generator()
    char_array = np.array([97, 98, 99])
    generator.char_set = char_array
    assert isinstance(generator.char_set, np.ndarray)
    assert np.array_equal(generator.char_set, char_array)


def test_generator_char_set_setter_with_empty_value():
    generator = Generator()
    with pytest.raises(ValueError, match="Charset should not be empty"):
        generator.char_set = ""


@patch("sprt.logger.logger.info")
def test_generator_generate(mock_logger):
    generator = Generator()
    distrib = Normal(mean=0.0, stdev=1.0)

    # Mock SINGLE_CHAR_SAMPLES_COUNT na wartość 1 dla uproszczenia testów
    with patch("sprt.config.SINGLE_CHAR_SAMPLES_COUNT", 1):
        result = generator.generate(size=10, distrib=distrib)

    assert isinstance(result, RandomText)
    assert len(result.text) == 10
    assert result.name == distrib.name
    assert result.distribution == distrib.name
    assert result.charset is generator.char_set
    assert isinstance(result.mean, float)
    assert isinstance(result.stdev, float)

    # Sprawdzenie, czy logger.info został wywołany
    mock_logger.assert_any_call("generation finished")


@patch("sprt.logger.logger.info")
def test_generator_generate_with_empty_char_set(mock_logger):
    generator = Generator()

    with pytest.raises(ValueError, match="Charset should not be empty"):
        generator.char_set = np.array([])

    distrib = Normal(mean=0.0, stdev=1.0)
    generator.generate(size=10, distrib=distrib)

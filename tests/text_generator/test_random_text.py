import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from sprt.text_generator.random_text import RandomText
from uuid import UUID
import json


def test_random_text_initialization():
    """Test poprawnej inicjalizacji obiektu RandomText."""
    text = np.array([1, 2, 3])
    charset = np.array([1, 2, 3])
    density_matrix = np.array([0.1, 0.2, 0.7])

    random_text = RandomText(
        name="test",
        text=text,
        distribution="test_distribution",
        length=3,
        mean=2.0,
        stdev=1.0,
        charset=charset,
        density_matrix=density_matrix,
        arguments={"arg1": "value1"},
    )

    assert random_text.name == "test"
    assert random_text.text is text
    assert random_text.distribution == "test_distribution"
    assert random_text.length == 3
    assert random_text.mean == 2.0
    assert random_text.stdev == 1.0
    assert np.array_equal(random_text.charset, charset)
    assert np.array_equal(random_text.density_matrix, density_matrix)
    assert random_text.arguments == {"arg1": "value1"}
    assert isinstance(random_text.id, UUID)


def test_random_text_to_json():
    text = np.array([1, 2, 3])
    random_text = RandomText(name="test", text=text, distribution="test_distribution")

    json_output = random_text.to_json()
    assert isinstance(json_output, str)

    parsed_output = json.loads(json_output)
    assert parsed_output["name"] == "test"
    assert parsed_output["distribution"] == "test_distribution"
    assert parsed_output["text"] == [1, 2, 3]


def test_random_text_from_json():
    json_input = '{"name": "test", "text": [1, 2, 3], "distribution": "test_distribution", "id": "12345678-1234-5678-1234-567812345678"}'
    random_text = RandomText.from_json(json_input)

    assert random_text.name == "test"
    assert np.array_equal(random_text.text, np.array([1, 2, 3]))
    assert random_text.distribution == "test_distribution"
    assert random_text.id == UUID("12345678-1234-5678-1234-567812345678")


def test_random_text_from_bytes_or_text_with_string():
    text = "abc"
    random_text = RandomText.from_bytes_or_text(value=text)

    assert random_text.name == "importowany"
    assert np.array_equal(random_text.text, np.array([97, 98, 99]))
    assert random_text.distribution == "importowany"


def test_random_text_async_density_matrix():
    text = np.array([1, 2, 2, 3, 3, 3])
    random_text = RandomText(name="test", text=text, distribution="test_distribution")
    random_text.wait()

    expected_density = np.array([1 / 6, 2 / 6, 3 / 6])
    assert np.allclose(random_text.density_matrix, expected_density, atol=1e-6)


@patch("sprt.logger.logger.info")
def test_random_text_logger(mock_logger):
    text = np.array([1, 2, 2, 3, 3, 3])
    random_text = RandomText(name="test", text=text, distribution="test_distribution")
    random_text.wait()

    # Sprawdź, czy logger wywołał odpowiedni komunikat
    mock_logger.assert_any_call("async computing done; '3' elements")

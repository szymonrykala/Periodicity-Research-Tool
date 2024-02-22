from functools import reduce
from itertools import repeat
from time import sleep
from uuid import UUID, uuid4

import pytest
from numpy import array, int64, ndarray

from sprt.text_generator import RandomText


def random_text_data():
    text = array(reduce(lambda xs, ys: xs + ys, tuple(repeat(tuple(range(44, 70)), 50))))
    return {
        "id": uuid4(),
        "arguments": {
            "stdev": 0.1,
            "mean": 1,
        },
        "length": len(text),
        "name": "test_name",
        "distribution": "Normal",
        "charset": array(list(range(44, 100))),
        "text": text,
        "mean": 1.01,
    }


@pytest.fixture
def random_text():
    data = random_text_data()
    text = RandomText(**data)
    text.wait()
    yield text


def test_random_text_construction(random_text: RandomText):
    if random_text._async_done is False:
        assert len(random_text.density_matrix) == 0
        assert random_text.mean is None
        assert random_text.stdev is None

    assert isinstance(random_text.id, UUID)
    assert isinstance(random_text.length, int)
    assert isinstance(random_text.text, ndarray)

    assert isinstance(random_text.charset, ndarray)
    assert isinstance(random_text.charset[0], int64)  # type: ignore

    assert isinstance(random_text.distribution, str)

    assert isinstance(random_text.text, ndarray)
    assert isinstance(random_text.text[0], int64)  # type: ignore

    assert isinstance(random_text.density_matrix, ndarray)
    assert isinstance(random_text.density_matrix[0], float)

    assert isinstance(random_text.stdev, float)
    assert isinstance(random_text.mean, float)


def test_random_text_de_serialization(random_text: RandomText):
    json_string = random_text.to_json()

    assert isinstance(json_string, str)

    parsed = RandomText.from_json(json_string)

    assert isinstance(parsed, RandomText)
    assert random_text.id == parsed.id
    assert random_text.distribution == parsed.distribution
    assert str(random_text.charset) == str(parsed.charset)
    assert str(random_text.text) == str(parsed.text)
    assert random_text.mean == parsed.mean
    assert random_text.stdev == parsed.stdev
    assert str(random_text.density_matrix) == str(parsed.density_matrix)
    assert random_text.arguments == parsed.arguments
    assert random_text.length == parsed.length


@pytest.mark.parametrize(
    "data",
    [
        [*tuple(range(44, 70)), *tuple(range(44, 70))],
        ",-./012345678,-./0123456789:;<=>?@ABCDE9:;<=>?@ABCDE",
    ],
)
def test_random_text_from_bytes_or_string(data):
    text = RandomText.from_bytes_or_text(data)

    assert text.name == "importowany"
    assert isinstance(text.distribution, str)

    assert isinstance(text.text, ndarray)
    assert isinstance(text.text[0], int64)  # type: ignore

    text.wait()

    assert isinstance(text.charset, ndarray)

    if isinstance(data, str):
        assert text.charset.tolist() == list(sorted(set(data.encode())))
    else:
        assert text.charset.tolist() == list(sorted(set(data)))

    assert isinstance(text.mean, float)
    assert isinstance(text.stdev, float)
    assert text.length == len(data)

    assert isinstance(text.density_matrix, ndarray)
    assert isinstance(text.density_matrix[0], float)

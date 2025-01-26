import numpy as np
import pytest

from sprt.text_generator.distributions import (
    Distribution,
    Exponential,
    Normal,
    Uniform,
    distributions_dict,
    distributions_list,
)


def test_distribution_abstract_methods():
    with pytest.raises(TypeError):
        instance = Distribution()


def test_normal_initialization():
    dist = Normal(mean=5.0, stdev=2.0)
    assert dist.args == {"mean": 5.0, "stdev": 2.0}
    assert dist.name == "Normalny"


def test_exponential_initialization():
    dist = Exponential(stdev=3.0)
    assert dist.args == {"stdev": 3.0}
    assert dist.name == "Wykładniczy"


def test_uniform_initialization():
    dist = Uniform(mean=4.0, stdev=2.0)
    assert dist.args == {"mean": 4.0, "stdev": 2.0}
    assert dist.name == "Jednostajny"


@pytest.mark.parametrize(
    "dist_class, kwargs, expected_length",
    [
        (Normal, {"mean": 0.0, "stdev": 1.0}, 10),
        (Exponential, {"stdev": 1.0}, 10),
        (Uniform, {"mean": 0.0, "stdev": 2.0}, 10),
    ],
)
def test_distribution_get(dist_class, kwargs, expected_length):
    dist = dist_class(**kwargs)
    values = dist.get(size=expected_length)
    assert isinstance(values, np.ndarray)
    assert len(values) == expected_length


def test_distribution_list_and_dict():
    assert distributions_list == [Normal, Exponential, Uniform]
    assert distributions_dict == {
        "Normalny": Normal,
        "Wykładniczy": Exponential,
        "Jednostajny": Uniform,
    }

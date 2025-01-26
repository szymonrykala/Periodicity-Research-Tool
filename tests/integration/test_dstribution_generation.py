import numpy as np
import pytest

from sprt.text_generator.distributions import Exponential, Normal, Uniform
from sprt.text_generator.generator import Generator
from sprt.text_generator.random_text import RandomText


@pytest.fixture
def generator_instance():
    return Generator()


@pytest.mark.parametrize(
    "distribution, dist_params, size",
    [
        (Normal, {"mean": 0.0, "stdev": 1.0}, 100),
        (Uniform, {"mean": 5.0, "stdev": 2.0}, 50),
        (Exponential, {"stdev": 2.0}, 200),
    ],
)
def test_text_generation_with_distributions(generator_instance, distribution, dist_params, size):
    distrib = distribution(**dist_params)
    generated_text = generator_instance.generate(size=size, distrib=distrib)

    assert isinstance(generated_text, RandomText)
    assert generated_text.length == size
    assert generated_text.distribution == distrib.name
    assert len(generated_text.text) == size
    assert isinstance(generated_text.text, np.ndarray)  # Zmieniono na numpy.ndarray


def test_generator_with_custom_charset(generator_instance):
    generator_instance.char_set = "xyz"
    distrib = Normal(mean=0.0, stdev=1.0)

    generated_text = generator_instance.generate(size=10, distrib=distrib)

    assert isinstance(generated_text, RandomText)
    assert len(generated_text.text) == 10
    # Sprawdź, czy wszystkie wygenerowane znaki są w zestawie znaków
    assert set(np.unique(generated_text.text)).issubset(set(ord(c) for c in "xyz"))


def test_generator_with_empty_charset(generator_instance):
    with pytest.raises(ValueError, match="Charset should not be empty"):
        generator_instance.char_set = ""


def test_generator_text_generation_stats(generator_instance):
    distrib = Normal(mean=10.0, stdev=2.0)
    generated_text = generator_instance.generate(size=1000, distrib=distrib)

    assert abs(generated_text.mean - 10.0) < 1.0  # Tolerancja na średnią
    assert abs(generated_text.stdev - 2.0) < 1.0  # Tolerancja na odchylenie


@pytest.mark.parametrize(
    "distribution, dist_params",
    [
        (Normal, {"mean": 0.0, "stdev": 1.0}),
        (Uniform, {"mean": 5.0, "stdev": 2.0}),
        (Exponential, {"stdev": 2.0}),
    ],
)
def test_generator_distribution_integration(generator_instance, distribution, dist_params):
    distrib = distribution(**dist_params)

    generated_text = generator_instance.generate(size=500, distrib=distrib)

    assert isinstance(generated_text, RandomText)
    assert generated_text.distribution == distrib.name
    assert generated_text.arguments == distrib.args


def test_generator_distribution_coverage(generator_instance):
    generator_instance.char_set = "xyz"
    distrib = Normal(mean=0.0, stdev=1.0)

    generated_text = generator_instance.generate(size=10000, distrib=distrib)

    assert isinstance(generated_text, RandomText)
    unique_chars = set(np.unique(generated_text.text))
    expected_chars = set(ord(c) for c in "xyz")
    # Sprawdź, czy dystrybucja dotknęła każdego znaku w char_set
    assert unique_chars == expected_chars, f"Missing chars: {expected_chars - unique_chars}"

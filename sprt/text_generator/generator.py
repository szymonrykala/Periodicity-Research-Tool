from random import choices

from numpy import array, histogram, ndarray

from sprt.config import DEFAULT_CHARSET, SINGLE_CHAR_SAMPLES_COUNT
from sprt.logger import logger

from .distributions import Distribution
from .random_text import RandomText


class Generator:
    def __init__(self) -> None:
        self._char_set: ndarray = array(tuple(set(DEFAULT_CHARSET.encode())))

    @property
    def char_set(self) -> ndarray:
        return self._char_set

    @char_set.setter
    def char_set(self, value: str | bytes | ndarray):
        if isinstance(value, str):
            value = value.encode()

        if len(array(tuple(set(value)))) == 0:
            raise ValueError("Charset should not be empty")

        self._char_set = array(tuple(set(value)))
        logger.info(f"Charset updated to {self._char_set}")

    def generate(self, size: int, distrib: Distribution):
        logger.info(f"starting generation {distrib.name=}, {size=}")
        random_samples = distrib.get(len(self._char_set) * SINGLE_CHAR_SAMPLES_COUNT)

        chars_probability, _ = histogram(
            a=random_samples, bins=tuple(range(0, len(self.char_set) + 1)), density=True
        )

        self._char_set.sort()
        generated_set = array(
            choices(population=self.char_set, weights=chars_probability.tolist(), k=size)
        )

        logger.info(f"generation finished")

        return RandomText(
            name=distrib.name,
            text=generated_set,
            stdev=round(random_samples.std(), 4),
            mean=round(random_samples.mean(), 4),
            charset=self.char_set,
            distribution=distrib.name,
            arguments=distrib.args,
            length=size,
        )

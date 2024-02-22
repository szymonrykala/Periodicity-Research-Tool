from random import choices

from numpy import array, histogram, ndarray

from sprt.config import DEFAULT_CHARSET, SINGLE_CHAR_SAMPLES_COUNT
from sprt.logger import logger

from .distributions import Distribution
from .random_text import RandomText


class Generator:
    """
    TODO: czy wykres powinien się przesuwać pod wpływem średniej??, nie do końca reaguje na stdev
    """

    def __init__(self) -> None:
        self._char_set: ndarray = array(tuple(set(DEFAULT_CHARSET.encode())))

    @property
    def char_set(self) -> ndarray:
        return self._char_set

    @char_set.setter
    def char_set(self, value: str | bytes | ndarray):
        if isinstance(value, str):
            value = value.encode()

        self._char_set = array(tuple(set(value)))
        logger.info(f"Charset updated to {self._char_set}")

    def __bounds_centers(self, bounds: list) -> list[float]:
        """calcuates centers of given bounds
        >>> __bounds_centers([1, 3, 5, 7])
        >>> [2, 4, 6]
        """

        def _inner():
            for i in range(1, len(bounds)):
                yield bounds[i - 1] + (
                    bounds[i] - bounds[i - 1]
                ) / 2  # wyliczanie środka przedziału

        return list(_inner())

    def generate(self, size: int, distrib: Distribution):
        logger.info(f"starting generation {distrib.name=}, {size=}")
        random_samples = distrib.get(len(self._char_set) * SINGLE_CHAR_SAMPLES_COUNT)

        multiplier = 1000
        multiplied = (random_samples * multiplier).astype("int64")

        chars_probability, _ = histogram(a=random_samples, bins=len(self._char_set), density=True)

        self._char_set.sort()
        generated_set = array(
            choices(population=self.char_set, weights=chars_probability.tolist(), k=size)
        )

        logger.info(f"generation finished")

        return RandomText(
            name=distrib.name,
            text=generated_set,
            # stdev=round(multiplied.std()/multiplier, 4),
            # mean=round(multiplied.mean()/multiplier, 4),
            charset=self.char_set,
            distribution=distrib.name,
            arguments=distrib.args,
            length=size,
        )

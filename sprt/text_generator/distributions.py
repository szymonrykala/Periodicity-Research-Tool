from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any

import numpy as np
from numpy.random import Generator, default_rng

from sprt.config import RANDOM_GENERATOR_SEED


class Distribution(ABC):
    np_rgen: Generator = default_rng(RANDOM_GENERATOR_SEED)
    _name: str = "base distribution class"

    def __init__(self, **kwargs):
        self.__args = kwargs

    @property
    def name(cls) -> str:
        return cls._name

    @cached_property
    def args(self) -> dict:
        return self.__args

    @classmethod
    @property
    def parameters(cls):
        return cls.__init__.__annotations__

    @abstractmethod
    def get(self, size: int) -> np.ndarray[Any, np.dtype[np.float64]]:
        ...


class Normal(Distribution):
    _name: str = "Normalny"

    def __init__(self, mean: float, stdev: float):
        super().__init__(mean=mean, stdev=stdev)

    def get(self, size: int):
        return self.np_rgen.normal(loc=self.args["mean"], scale=self.args["stdev"], size=size)


class Exponential(Distribution):
    _name: str = "Wykładniczy"

    def __init__(self, stdev: float):
        super().__init__(stdev=stdev)

    def get(self, size: int):
        return self.np_rgen.exponential(scale=self.args["stdev"], size=size)


class Uniform(Distribution):
    _name: str = "Jednostajny"

    def __init__(self, mean: float, stdev: float):
        super().__init__(mean=mean, stdev=stdev)

    def get(self, size: int):
        offset = self.args["stdev"] / 2
        return self.np_rgen.uniform(
            low=self.args["mean"] - offset,
            high=self.args["mean"] + offset,
            size=size,
        )


distributions_list: list[type[Distribution]] = [Normal, Exponential, Uniform]
distributions_dict: dict[str, type[Distribution]] = {d._name: d for d in distributions_list}

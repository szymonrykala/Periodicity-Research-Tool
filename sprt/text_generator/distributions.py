from abc import ABC, abstractmethod
from functools import cached_property
from math import sqrt
from typing import Any

import numpy as np
from numpy.random import Generator, default_rng


class Distribution(ABC):
    np_rgen: Generator = default_rng()
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
    def get(self, size: int) -> np.ndarray[Any, np.dtype[np.float64]]: ...


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
        stdev = self.args["stdev"]
        return self.np_rgen.uniform(
            low=self.args["mean"] - sqrt(3) * stdev,
            high=self.args["mean"] + sqrt(3) * stdev,
            size=size,
        )


distributions_list: list[type[Distribution]] = [Normal, Exponential, Uniform]
distributions_dict: dict[str, type[Distribution]] = {d._name: d for d in distributions_list}

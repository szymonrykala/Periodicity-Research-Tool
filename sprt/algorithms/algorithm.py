from dataclasses import dataclass, field
from functools import cached_property, wraps
from importlib import import_module
from typing import Callable, Optional

from numpy import ndarray


def _args_builder(func):
    """Merge arguments passed to the algorithm main function with default algorithm arguments"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        data = {}
        for arg in self.args:
            if arg.name in kwargs:
                data[arg.name] = kwargs[arg.name]
            else:
                data[arg.name] = arg.default
        return func(self, *args, **data)

    return wrapper


@dataclass
class Result:
    raw_time: float
    pattern: Optional[ndarray] = None
    time: Optional[float] = None
    value: list[int] = field(default_factory=list)

    def __init__(self, time: float, value: list[int] = [], pattern: Optional[ndarray] = None):
        self.value = value
        self.raw_time = time
        self.pattern = pattern

    def refer(self, ref_run: "Result"):
        self.time = self.raw_time / ref_run.raw_time


@dataclass
class AlgArgument:
    name: str
    type: type
    default: Optional[str | int] = None

    def __str__(self) -> str:
        return f"{self.name}: {self.type.__name__} = {self.default}"  # type: ignore


class Algorithm:
    def __init__(
        self,
        name: str,
        description: str,
        main_fn: Callable,
    ) -> None:
        self.name = name
        self.description = description
        self.__main = main_fn

    @cached_property
    def args(self):
        defaults = self.__main.__kwdefaults__ or {}
        return tuple(
            AlgArgument(name=name, type=_type, default=defaults.get(name))
            for name, _type in self.__main.__annotations__.items()
        )

    def __str__(self):
        return self.name

    @_args_builder
    def run(self, **arguments: ndarray) -> list[int]:
        return self.__main(**arguments)


class AlgorithmStore:
    def __init__(self):
        self.__system_mod = import_module(".system", "sprt.algorithms")
        self.__library_mod = import_module(".library", "sprt.algorithms")

    @cached_property
    def time_reference_algorithm(self):
        alg = self.__system_mod.time_reference_algorithm
        return Algorithm(name=alg.__alg_name__, description=alg.__doc__, main_fn=alg.main)

    @cached_property
    def algorithms(self):
        def _wrap():
            for name in self.__library_mod.__all__:
                mod = import_module(".".join((self.__library_mod.__name__, name)))
                yield Algorithm(
                    name=mod.__alg_name__,
                    description=mod.__doc__ or "Brak opisu",
                    main_fn=mod.main,
                )

        return list(_wrap())

    @cached_property
    def algorithms_dict(self):
        return {alg.name: alg for alg in self.algorithms}

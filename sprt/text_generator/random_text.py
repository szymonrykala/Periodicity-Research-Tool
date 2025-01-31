import json
import os
from collections import Counter
from dataclasses import asdict, dataclass, field
from functools import cached_property
from statistics import mean, stdev
from threading import Thread
from time import sleep
from typing import Iterable, Optional
from uuid import UUID, uuid1, uuid4

from numpy import array, floating, integer, ndarray

from sprt.logger import logger
from sprt.utils import bytes_to_str


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, integer):
            return int(obj)
        if isinstance(obj, floating):
            return float(obj)
        if isinstance(obj, ndarray):
            return obj.tolist()
        if isinstance(obj, UUID):
            return str(obj)
        return super(NpEncoder, self).default(obj)


@dataclass
class RandomText:
    name: str
    text: ndarray
    distribution: str
    length: int = field(default=0)
    mean: Optional[float] = None
    stdev: Optional[float] = None
    charset: ndarray = field(default_factory=lambda: array([]))
    density_matrix: ndarray = field(default_factory=lambda: array([]))
    arguments: dict = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    _binary: bool = field(default=False)
    _async_done: bool = field(default=False)

    @cached_property
    def parsed_text(self) -> str:
        if self._binary:
            return bytes(self.text.tolist())

        return bytes_to_str(self.text)

    @cached_property
    def parsed_charset(self) -> str:
        return bytes_to_str(self.charset)

    @classmethod
    def from_json(cls, string: str):
        obj = json.loads(string)
        for field in ("text", "charset", "density_matrix"):
            if field in obj:
                obj[field] = array(obj[field])
            else:
                obj[field] = array([])

        obj["id"] = UUID(obj["id"])

        return cls(**obj)

    @classmethod
    def from_bytes(cls, value: bytes, name: str = "importowany"):
        return cls(
            name=name.split(os.sep)[-1],
            text=array(tuple(value)),
            distribution="importowany",
            _binary=True,
        )

    @classmethod
    def from_text(cls, value: str, name: str = "importowany"):
        return cls(
            name=name.split(os.sep)[-1],
            text=array(tuple(value.encode())),
            distribution="importowany",
            _binary=False,
        )

    @classmethod
    def from_bytes_or_text(cls, value: ndarray | Iterable | str, name: str = "importowany"):
        if isinstance(value, str):
            value = tuple(value.encode())

        if not isinstance(value, ndarray):
            value = array(value)

        return cls(
            name=name.split(os.sep)[-1],
            text=value,
            distribution="importowany",
            _binary=True,
        )

    def __post_init__(self):
        if not self._async_done:
            Thread(target=self.__async_compute_density_matrix).start()

    def __hash__(self):
        return hash(str(self.text))

    def __async_compute_density_matrix(self):
        logger.info("async computing if needed")
        i = 0

        if self.length == 0:
            self.length = len(self.text)
            i += 1

        if len(self.charset) == 0:
            self.charset = array(tuple(set(self.text)))
            logger.debug(f"charset set to {self.charset}")
            i += 1

        if len(self.density_matrix) == 0:
            probability = {k: v / self.length for k, v in Counter(self.text.tolist()).items()}
            self.density_matrix = array(
                tuple({char: probability.get(char, 0) for char in self.charset}.values())
            )
            i += 1

        self._async_done = True
        logger.info(f"async computing done; '{i}' elements")

    def to_json(self):
        return json.dumps(asdict(self), cls=NpEncoder)

    def wait(self):
        while not self._async_done:
            sleep(0.01)

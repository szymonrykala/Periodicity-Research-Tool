from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from copy import copy
from dataclasses import dataclass
from functools import cached_property
from threading import Thread
from time import time
from tkinter import BooleanVar
from typing import Iterable

from sprt.algorithms.algorithm import Algorithm
from sprt.logger import logger
from sprt.text_generator.random_text import RandomText


@dataclass
class AnalysisResult:
    indexes: list[int]
    pattern: RandomText
    index_offset: list[int]
    index_offset_groups: dict[int, int]


class PeriodicityAnalysis:
    def __init__(self, text_set: RandomText, algorithm: Algorithm, patterns: list[RandomText]):
        self.__text_set = text_set
        self.__algorithm = algorithm
        self.__patterns = patterns

        self.ready = BooleanVar(value=False)
        self.results: list[AnalysisResult] = []

    @property
    def name(self):
        return self.__text_set.name

    @property
    def text_set(self):
        return self.__text_set

    @property
    def algorithm(self):
        return self.__algorithm.name

    @cached_property
    def patterns_count(self):
        return len(self.__patterns)

    @cached_property
    def hash(self):
        return hash((self.algorithm, self.__text_set.id, map(lambda v: v.id, self.__patterns)))

    def __find_indexes(self, pattern: RandomText) -> list[int]:
        return self.__algorithm.run(text=self.__text_set.text, pattern=pattern.text)

    def __count_occurrences_offsets(self, indexes: list[int]) -> list[int]:
        """
        indexes = [3, 5, 6 ,9 ,10]
        out = [2, 1, 3, 1]
        """
        if not indexes:
            return []

        indexes_cp = copy(indexes)

        def _job():
            last = indexes_cp.pop(0)
            for i in indexes_cp:
                yield i - last
                last = i

        return list(_job())

    def __count_index_offset_groups(self, offsets: Iterable[int]):
        return dict(
            sorted(
                Counter(offsets).items(),
                key=lambda item: item[0],
            )
        )

    def _pattern_occurrences_job(self, pattern: RandomText):
        result = self.__find_indexes(pattern)

        offsets = self.__count_occurrences_offsets(result)
        analysis = AnalysisResult(
            indexes=result,
            pattern=pattern,
            index_offset=offsets,
            index_offset_groups=self.__count_index_offset_groups(offsets),
        )
        logger.debug(f"job for pattern '{pattern.parsed_text}' done")
        return analysis

    def patterns_occurrences(self):
        with ThreadPoolExecutor(4) as exec:
            self.results = list(exec.map(self._pattern_occurrences_job, self.__patterns))
            self.results.sort(key=lambda item: len(item.indexes), reverse=True)

        logger.info(f"async analysis with '{self.__algorithm}' for '{self.__text_set.name}' DONE")
        self.ready.set(True)

    def run_async(self):
        """Starts async analysis."""
        logger.info(f"START async analysis with '{self.__algorithm}' for '{self.__text_set.name}'")
        Thread(target=self.patterns_occurrences).start()

    def measure_single_pattern_run(self, pattern: RandomText) -> float:
        """
        This version is used for performance analysis.
        """
        start = time()
        self._pattern_occurrences_job(pattern)
        return time() - start

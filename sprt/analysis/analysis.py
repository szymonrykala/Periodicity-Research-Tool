from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import cached_property
from threading import Thread
from tkinter import BooleanVar

from sprt.algorithms.algorithm import Algorithm, Result
from sprt.logger import logger
from sprt.text_generator.random_text import RandomText


@dataclass
class AnalysisResult:
    algorithm: Result
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

    @property
    def patterns_count(self):
        return len(self.__patterns)

    @cached_property
    def hash(self):
        return hash((self.algorithm, self.__text_set.id, map(lambda v: v.id, self.__patterns)))

    def __find_indexes(self, pattern: RandomText) -> Result:
        print(pattern)
        return self.__algorithm.run(text=self.__text_set.text, pattern=pattern.text)

    def __count_occurrences_offsets(self, indexes: list[int]) -> list[int]:
        """
        indexes = [3, 5, 6 ,9 ,10]
        out = [2, 1, 3, 1]
        """
        if not indexes:
            return []

        def _job():
            last = indexes.pop(0)
            for i in indexes:
                yield i - last
                last = i

        return list(_job())

    def __count_index_offset_groups(self, offsets: list[int]):
        return dict(
            sorted(
                Counter(offsets).items(),
                key=lambda item: item[0],
            )
        )

    def _patterns_occurrences_job(self, pattern: RandomText):
        result = self.__find_indexes(pattern)

        offsets = self.__count_occurrences_offsets(result.value)
        analysis = AnalysisResult(
            algorithm=result,
            index_offset=offsets,
            index_offset_groups=self.__count_index_offset_groups(offsets),
        )
        logger.info(f"job for pattern '{pattern.parsed_text}' done")
        return analysis

    def patterns_occurrences(self):
        with ThreadPoolExecutor(4) as exec:
            jobs = exec.map(self._patterns_occurrences_job, self.__patterns)
            self.results = list(jobs)

        logger.info(f"async analysis with '{self.__algorithm}' for '{self.__text_set.name}' DONE")
        self.ready.set(True)

    def run(self):
        """starts async analysis"""
        logger.info(f"START async analysis with '{self.__algorithm}' for '{self.__text_set.name}'")
        Thread(target=self.patterns_occurrences).start()

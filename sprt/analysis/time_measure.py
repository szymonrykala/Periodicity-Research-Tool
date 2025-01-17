from dataclasses import dataclass
from functools import cached_property
from statistics import mean, stdev
from time import time
from tkinter import BooleanVar, StringVar
from typing import Dict, Iterable, Optional

from sprt.algorithms import Algorithm, AlgorithmStore
from sprt.analysis.analysis import PeriodicityAnalysis
from sprt.config import (
    ENV_STABLE_WAIT_TIME,
    ENV_TIME_DEVIATION_REPEATS,
    ENV_TIME_DEVIATION_THRESHOLD,
    TIME_MEASURE_MEAN_COUNT,
)
from sprt.logger import logger
from sprt.text_generator import RandomText
from sprt.utils import bytes_to_str


@dataclass
class ResultsMean:
    stdev: float
    time: float

    def __init__(self, measures: Iterable[float]):
        work_time = tuple(measures)
        self.time = mean(work_time)
        self.stdev = stdev(work_time)

    def refer_env(self, ref_time: float) -> "ResultsMean":
        self.time = self.time / ref_time
        return self


@dataclass
class RunPerformanceData:
    stdev: list[float]
    time: list[float]

    def __init__(self, results_list: Iterable[ResultsMean]):
        self.stdev, self.time = [], []

        for r in results_list:
            self.stdev.append(r.stdev)
            self.time.append(r.time)


TextRunResults = Dict[str, RunPerformanceData]


@dataclass
class PerformanceResultsData:
    patterns_length: list[int]
    patterns_text: list[str]
    data: dict[str, TextRunResults]

    def __init__(self, data, patterns):
        self.data = data
        self.patterns_length = list(p.length for p in patterns)
        self.patterns_text = list(bytes_to_str(p.text) for p in patterns)

    @cached_property
    def transformed_data(self):
        """
        {
            text_set_name: {
                algorithm_name: RunPerformanceData<stdev, mean>
                ...
            },
            ...
        }
        """
        out = {}
        for alg_name, text_sets in self.data.items():
            for text_set_name, measurements in text_sets.items():
                if text_set_name not in out:
                    out[text_set_name] = {alg_name: measurements}
                else:
                    out[text_set_name][alg_name] = measurements
        return out


class EnvNotStableError(EnvironmentError):
    def __init__(self):
        super().__init__("Could not reach required deviation threshold")


class TimeMeasurement:
    def __init__(
        self,
        algorithms: Iterable[Algorithm],
        text_sets: Iterable[RandomText],
        patterns: Iterable[RandomText],
    ):
        self.__text_sets = text_sets
        self.__algorithms = algorithms
        self.__patterns = sorted(patterns, key=lambda p: p.length)
        self.__env_ref_algorithm = AlgorithmStore().time_reference_algorithm
        self.__env_ref_algorithm_time: Optional[float] = None

        self.__results: Optional[PerformanceResultsData] = None
        self.message = StringVar(value="")
        self.ready = BooleanVar(value=False)

    @cached_property
    def results(self):
        """
        {
            algorithm_name: {
                text_set_name: RunPerformanceData<stdev, mean>
                ...
            },
            ...
        }
        """
        return self.__results

    @property
    def time_reference(self) -> float:
        if not self.__env_ref_algorithm_time:
            raise RuntimeError("Environment reference was not taken")
        return self.__env_ref_algorithm_time
    
    @time_reference.setter
    def time_reference(self, value:float):
        self.__env_ref_algorithm_time = value

    def __get_reference_measure(self) -> tuple[float, float]:
        def _measure():
            start = time()
            self.__env_ref_algorithm.run()
            return time() - start

        measured_times = [_measure() for _ in range(0, TIME_MEASURE_MEAN_COUNT)]
        return mean(measured_times), stdev(measured_times)

    def _is_environment_stable(self):
        mean_time = 0
        deviation = 1
        tries = 0

        start_time = time()

        logger.info(f"Badanie stabilności środowiska ...")
        while tries < ENV_TIME_DEVIATION_REPEATS:
            mean_time, deviation = self.__get_reference_measure()
            self.message.set(f"Badanie stabilności środowiska: stdev={deviation}")
            logger.debug(
                f"Badanie środowiska: wymagana dewiacja < {ENV_TIME_DEVIATION_THRESHOLD}, aktualnie = {deviation}"
            )
            if deviation < ENV_TIME_DEVIATION_THRESHOLD:
                tries += 1
            else:
                tries = 0
                if (time() - start_time) > ENV_STABLE_WAIT_TIME:
                    logger.error("Środowisko jest zbyt niestabilne by przeprowadzić pomiar.")
                    self.message.set("Środowisko jest zbyt niestabilne by przeprowadzić pomiar.")
                    self.ready.set(False)
                    raise EnvNotStableError()

        self.time_reference = mean_time
        logger.info(f"Time reference has been set to '{self.time_reference}'")
        return True

    def __run_for_pattern(self, analysis: PeriodicityAnalysis, pattern: RandomText) -> ResultsMean:
        return ResultsMean(
            (
                analysis.measure_single_pattern_run(pattern=pattern)
                for _ in range(0, TIME_MEASURE_MEAN_COUNT)
            )
        ).refer_env(self.time_reference)

    def __run_for_algorithm(self, algorithm: Algorithm) -> TextRunResults:
        results = {}
        for text_set in self.__text_sets:
            analysis = PeriodicityAnalysis(text_set=text_set, algorithm=algorithm, patterns=[])
            results[text_set.name] = RunPerformanceData(
                (self.__run_for_pattern(analysis, pattern) for pattern in self.__patterns)
            )
        return results

    def run(self):
        if self._is_environment_stable():
            logger.info("Pomiar wydajności algorytmów rozpoczęty")
            self.message.set("Pomiar rozpoczęty")

            self.__results = PerformanceResultsData(
                patterns=self.__patterns,
                data={
                    algorithm.name: self.__run_for_algorithm(algorithm)
                    for algorithm in self.__algorithms
                },
            )

            logger.info("Pomiar wydajności algorytmów zakończony")
            self.message.set("Pomiary działania zakończone")
            self.ready.set(True)

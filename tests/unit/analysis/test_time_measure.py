import tkinter as tk
from statistics import mean, stdev
from unittest.mock import MagicMock, patch

import pytest

from sprt.algorithms import Algorithm
from sprt.analysis.time_measure import (
    EnvNotStableError,
    PerformanceResultsData,
    ResultsMean,
    RunPerformanceData,
    TimeMeasurement,
)
from sprt.text_generator import RandomText


@pytest.fixture(scope="module", autouse=True)
def tkinter_root():
    root = tk.Tk()
    root.withdraw()  # Ukryj okno główne
    yield
    root.destroy()


@pytest.mark.parametrize(
    "measures, expected_mean, expected_stdev",
    [
        ([1.0, 1.5, 2.0], mean([1.0, 1.5, 2.0]), stdev([1.0, 1.5, 2.0]) / mean([1.0, 1.5, 2.0])),
        ([2.0, 2.0, 2.0], 2.0, 0.0),
    ],
)
def test_results_mean_initialization(measures, expected_mean, expected_stdev):
    result = ResultsMean(measures)
    assert result.time == expected_mean
    assert result.rel_stdev == expected_stdev


@pytest.mark.parametrize(
    "measures, ref_time, expected_mean",
    [
        ([1.0, 2.0, 3.0], 2.0, mean([1.0, 2.0, 3.0]) / 2.0),
        ([4.0, 4.0, 4.0], 4.0, 1.0),
    ],
)
def test_results_mean_refer_env(measures, ref_time, expected_mean):
    result = ResultsMean(measures)
    result.refer_env(ref_time)
    assert result.time == expected_mean


@pytest.mark.parametrize(
    "results, expected_stdev, expected_mean",
    [
        (
            [ResultsMean([1.0, 2.0]), ResultsMean([1.5, 2.5])],
            [stdev([1.0, 2.0]) / mean([1.0, 2.0]), stdev([1.5, 2.5]) / mean([1.5, 2.5])],
            [mean([1.0, 2.0]), mean([1.5, 2.5])],
        ),
        (
            [ResultsMean([3.0, 3.0]), ResultsMean([4.0, 4.0])],
            [0.0, 0.0],
            [3.0, 4.0],
        ),
    ],
)
def test_run_performance_data_initialization(results, expected_stdev, expected_mean):
    performance_data = RunPerformanceData(results)

    assert pytest.approx(performance_data.rel_stdev, rel=1e-6) == expected_stdev
    assert performance_data.time == expected_mean


@pytest.mark.parametrize(
    "data, patterns, expected_lengths, expected_texts",
    [
        (
            {"alg1": {"text1": MagicMock(spec=RunPerformanceData)}},
            [MagicMock(length=5, text="abc".encode())],
            [5],
            ["abc"],
        ),
        (
            {"alg1": {"text1": MagicMock(spec=RunPerformanceData)}},
            [MagicMock(length=10, text="def".encode())],
            [10],
            ["def"],
        ),
    ],
)
def test_performance_results_data_initialization(data, patterns, expected_lengths, expected_texts):
    performance_data = PerformanceResultsData(data, patterns)
    assert performance_data.patterns_length == expected_lengths
    assert performance_data.patterns_text == expected_texts


def test_env_not_stable_error():
    with pytest.raises(EnvNotStableError, match="Could not reach required deviation threshold"):
        raise EnvNotStableError()


@patch("sprt.analysis.time_measure.AlgorithmStore")
def test_time_measurement_initialization(mock_algorithm_store):
    algorithms = [MagicMock(spec=Algorithm)]
    text_sets = [MagicMock(spec=RandomText)]
    patterns = [MagicMock(spec=RandomText)]
    mock_algorithm_store().time_reference_algorithm = MagicMock(spec=Algorithm)

    time_measurement = TimeMeasurement(algorithms, text_sets, patterns)
    assert time_measurement.ready.get() is False


@patch("sprt.analysis.time_measure.TimeMeasurement._is_environment_stable")
@patch("sprt.analysis.time_measure.PeriodicityAnalysis")
@patch("sprt.analysis.time_measure.AlgorithmStore")
def test_time_measurement_run(mock_algorithm_store, mock_periodicity_analysis, mock_is_env_stable):
    mock_is_env_stable.return_value = True
    mock_algorithm_store().time_reference_algorithm = MagicMock(spec=Algorithm)

    algorithms = [MagicMock(spec=Algorithm)]
    algorithms[0].name = "alg1"
    text_sets = [MagicMock(spec=RandomText, name="text1")]
    patterns = [MagicMock(spec=RandomText, length=5, text=b"abc")]

    time_measurement = TimeMeasurement(algorithms, text_sets, patterns)
    with patch.object(time_measurement, "_TimeMeasurement__run_for_algorithm") as mock_run_alg:
        mock_run_alg.return_value = {"text1": MagicMock()}
        time_measurement.run()

    assert time_measurement.ready.get() is True

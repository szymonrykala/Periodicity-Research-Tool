from unittest.mock import MagicMock, patch

import pytest

from sprt.algorithms.algorithm import Algorithm
from sprt.analysis.analysis import AnalysisResult, PeriodicityAnalysis
from sprt.text_generator.random_text import RandomText


@pytest.fixture
def mock_random_text():
    """Fixture dla mockowanego obiektu RandomText."""
    mock_text = MagicMock(spec=RandomText)
    mock_text.name = "mock_text"
    mock_text.text = [1, 2, 3, 4, 2, 3]
    mock_text.id = 12345
    return mock_text


@pytest.fixture
def mock_algorithm():
    """Fixture dla mockowanego algorytmu."""
    mock_alg = MagicMock(spec=Algorithm)
    mock_alg.name = "mock_algorithm"
    mock_alg.run.return_value = [1, 4]
    return mock_alg


@pytest.fixture
def mock_patterns():
    """Fixture dla listy mockowanych wzorców."""
    pattern1 = MagicMock(spec=RandomText)
    pattern1.text = [2, 3]
    pattern1.id = 6789
    pattern1.parsed_text = "mock_pattern_1"

    pattern2 = MagicMock(spec=RandomText)
    pattern2.text = [3, 4]
    pattern2.id = 9876
    pattern2.parsed_text = "mock_pattern_2"

    return [pattern1, pattern2]


@pytest.fixture
@patch("sprt.analysis.analysis.BooleanVar")
def periodicity_analysis(mock_boolean_var, mock_random_text, mock_algorithm, mock_patterns):
    """Fixture dla instancji PeriodicityAnalysis."""
    mock_boolean_var.return_value = MagicMock()
    return PeriodicityAnalysis(
        text_set=mock_random_text,
        algorithm=mock_algorithm,
        patterns=mock_patterns,
    )


def test_periodicity_analysis_initialization(
    periodicity_analysis, mock_random_text, mock_algorithm, mock_patterns
):
    assert periodicity_analysis.text_set == mock_random_text
    assert periodicity_analysis.algorithm == mock_algorithm.name
    assert periodicity_analysis.patterns_count == len(mock_patterns)
    # Sprawdzenie wartości początkowej ready
    assert periodicity_analysis.ready.get.call_count == 0


def test_periodicity_analysis_find_indexes(periodicity_analysis, mock_patterns):
    result = periodicity_analysis._PeriodicityAnalysis__find_indexes(mock_patterns[0])
    assert result == [1, 4]
    periodicity_analysis._PeriodicityAnalysis__algorithm.run.assert_called_once_with(
        text=periodicity_analysis.text_set.text, pattern=mock_patterns[0].text
    )


@pytest.mark.parametrize(
    "indexes, expected_offsets",
    [
        ([3, 5, 6, 9, 10], [2, 1, 3, 1]),
        ([1, 4, 7], [3, 3]),
        ([], []),
    ],
)
def test_periodicity_analysis_count_occurrences_offsets(
    periodicity_analysis, indexes, expected_offsets
):
    result = periodicity_analysis._PeriodicityAnalysis__count_occurrences_offsets(indexes)
    assert result == expected_offsets


@pytest.mark.parametrize(
    "offsets, expected_groups",
    [
        ([2, 1, 3, 1], {1: 2, 2: 1, 3: 1}),
        ([3, 3, 3], {3: 3}),
        ([], {}),
    ],
)
def test_periodicity_analysis_count_index_offset_groups(
    periodicity_analysis, offsets, expected_groups
):
    result = periodicity_analysis._PeriodicityAnalysis__count_index_offset_groups(offsets)
    assert result == expected_groups


@patch("sprt.analysis.analysis.ThreadPoolExecutor")
def test_patterns_occurrences(mock_executor, periodicity_analysis, mock_patterns):
    mock_executor.return_value.__enter__.return_value.map.return_value = [
        MagicMock(spec=AnalysisResult, indexes=[]) for _ in mock_patterns
    ]

    periodicity_analysis.patterns_occurrences()

    assert len(periodicity_analysis.results) == len(mock_patterns)
    assert periodicity_analysis.ready.get()


@patch("sprt.analysis.analysis.Thread")
def test_run_async(mock_thread, periodicity_analysis):
    periodicity_analysis.run_async()
    mock_thread.assert_called_once_with(target=periodicity_analysis.patterns_occurrences)


def test_measure_single_pattern_run(periodicity_analysis, mock_patterns):
    with patch("sprt.analysis.analysis.time", side_effect=[0, 0.5]):
        result = periodicity_analysis.measure_single_pattern_run(mock_patterns[0])
    assert result == 0.5

import pytest
from unittest.mock import patch, MagicMock
from sprt.analysis.analysis import PeriodicityAnalysis
from sprt.analysis.time_measure import TimeMeasurement
from sprt.text_generator import RandomText
from sprt.algorithms.algorithm import Algorithm


@pytest.fixture
def mock_boolean_var():
    with patch("sprt.analysis.analysis.BooleanVar") as MockBooleanVar:
        MockBooleanVar.return_value.get.return_value = False
        yield MockBooleanVar


@pytest.fixture
def mock_time_measurement_boolean_var():
    with patch("sprt.analysis.time_measure.BooleanVar") as MockBooleanVar:
        MockBooleanVar.return_value.get.return_value = False
        yield MockBooleanVar


@pytest.fixture
def mock_algorithm():
    algorithm = MagicMock(spec=Algorithm)
    algorithm.name = "TestAlgorithm"
    algorithm.run.return_value = [1, 4, 7]  # Poprawione wyniki
    return algorithm


@pytest.fixture
def random_text():
    random_text = MagicMock(spec=RandomText)
    random_text.name = "TestTextSet"
    random_text.id = "1234"
    random_text.text = "abcdefgh"
    return random_text


@pytest.fixture
def random_patterns():
    pattern1 = MagicMock(spec=RandomText)
    pattern1.name = "Pattern1"
    pattern1.id = "5678"
    pattern1.text = "abc"
    pattern1.length = 3

    pattern2 = MagicMock(spec=RandomText)
    pattern2.name = "Pattern2"
    pattern2.id = "91011"
    pattern2.text = "def"
    pattern2.length = 3

    return [pattern1, pattern2]


@pytest.fixture
def mock_algorithms():
    algorithm1 = MagicMock(spec=Algorithm)
    algorithm1.name = "Algorithm1"
    algorithm1.run = MagicMock(return_value=[1, 2, 3])

    algorithm2 = MagicMock(spec=Algorithm)
    algorithm2.name = "Algorithm2"
    algorithm2.run = MagicMock(return_value=[4, 5, 6])

    return [algorithm1, algorithm2]


@pytest.fixture
def mock_text_sets():
    text1 = MagicMock(spec=RandomText)
    text1.name = "Text1"
    text1.id = "1234"
    text1.text = "abcdefgh"

    text2 = MagicMock(spec=RandomText)
    text2.name = "Text2"
    text2.id = "5678"
    text2.text = "ijklmnop"

    return [text1, text2]


def test_periodicity_analysis_execution(
    mock_boolean_var, mock_algorithm, random_text, random_patterns
):
    with patch.object(
        PeriodicityAnalysis,
        "_PeriodicityAnalysis__find_indexes",
        return_value=[1, 4, 7],
    ) as mock_find_indexes:
        analysis = PeriodicityAnalysis(
            text_set=random_text, algorithm=mock_algorithm, patterns=random_patterns
        )

        analysis.patterns_occurrences()

        assert len(analysis.results) == len(random_patterns)
        for result in analysis.results:

            assert isinstance(result.indexes, list)
            assert result.indexes == [7]  # Oczekiwane dane

        mock_find_indexes.assert_called()
        assert mock_find_indexes.call_count == len(random_patterns)


@patch("sprt.analysis.time_measure.StringVar")
@patch("sprt.analysis.time_measure.BooleanVar")
@patch("sprt.analysis.time_measure.TIME_MEASURE_MEAN_COUNT", 3)
@patch("sprt.analysis.time_measure.ENV_TIME_DEVIATION_THRESHOLD", 0.1)
def test_time_measurement_execution(
    mock_time_measurement_boolean_var,
    mock_string_var,
    mock_algorithms,
    mock_text_sets,
    random_patterns,
):
    with patch("sprt.analysis.analysis.BooleanVar") as MockBooleanVar:
        MockBooleanVar.return_value.get.return_value = False
        time_measure = TimeMeasurement(
            algorithms=mock_algorithms,
            text_sets=mock_text_sets,
            patterns=random_patterns,
        )

        time_measure.run()

        assert time_measure.results is not None
        for (
            algorithm_name,
            text_set_results,
        ) in time_measure.results.transformed_data.items():
            for text_set_name, measurements in text_set_results.items():
                assert isinstance(measurements.time, list)
                assert isinstance(measurements.rel_stdev, list)

import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from sprt.algorithms.algorithm import Result, Algorithm, AlgorithmStore, AlgArgument


# Testy dla Result
@pytest.mark.parametrize(
    "time, value, pattern",
    [
        (1.23, [1, 2, 3], np.array([0, 1])),
        (0.0, [], None),
        (5.67, [7, 8, 9], np.array([1, 0, 1])),
    ],
)
def test_result_initialization(time, value, pattern):
    result = Result(time=time, value=value, pattern=pattern)
    assert result.raw_time == time
    assert result.value == value
    assert (result.pattern is None and pattern is None) or np.array_equal(
        result.pattern, pattern
    )
    assert result.time is None


@pytest.mark.parametrize(
    "ref_time, time, expected_time",
    [
        (2.0, 4.0, 2.0),
        (1.0, 1.0, 1.0),
        (10.0, 5.0, 0.5),
    ],
)
def test_result_refer(ref_time, time, expected_time):
    ref_result = Result(time=ref_time)
    result = Result(time=time)
    result.refer(ref_result)
    assert result.time == expected_time


# Testy dla AlgArgument
@pytest.mark.parametrize(
    "name, type_, default, expected_str",
    [
        ("test", int, 42, "test: int = 42"),
        ("param", str, "default", "param: str = default"),
        ("flag", bool, None, "flag: bool = None"),
    ],
)
def test_alg_argument(name, type_, default, expected_str):
    arg = AlgArgument(name=name, type=type_, default=default)
    assert arg.name == name
    assert arg.type == type_
    assert arg.default == default
    assert str(arg) == expected_str


# Testy dla Algorithm
def mock_algorithm_main_fn(param1: int = 10, param2: str = "default"):
    return [param1, param2]


@pytest.mark.parametrize(
    "param1, param2, expected",
    [
        (20, "test", [20, "test"]),
        (0, "empty", [0, "empty"]),
        (42, "meaning", [42, "meaning"]),
    ],
)
def test_algorithm_run(param1, param2, expected):
    algorithm = Algorithm(
        name="Test Algorithm",
        description="An example algorithm",
        main_fn=mock_algorithm_main_fn,
    )
    result = algorithm.run(param1=param1, param2=param2)
    assert result == expected


def test_algorithm_args():
    algorithm = Algorithm(
        name="Test Algorithm",
        description="An example algorithm",
        main_fn=mock_algorithm_main_fn,
    )
    args = algorithm.args
    assert len(args) == 2


@pytest.mark.parametrize(
    "alg_name, alg_doc, alg_fn",
    [
        ("Ref Algorithm", "Reference algorithm", lambda x: x),
        ("Mock Algorithm", "Mocked description", lambda x: x * 2),
    ],
)
@patch("importlib.import_module")
def test_algorithm_store_time_reference_algorithm(
    mock_import_module, alg_name, alg_doc, alg_fn
):
    # Przygotowanie mocków
    mock_system = MagicMock()
    mock_alg = MagicMock()
    mock_alg.__alg_name__ = alg_name
    mock_alg.__doc__ = alg_doc
    mock_alg.main = alg_fn
    mock_system.time_reference_algorithm = mock_alg

    # Mockowanie funkcji import_module
    def side_effect(name, package):
        if name == ".system" and package == "sprt.algorithms":
            return mock_system
        raise ImportError(f"Module {name} not found")

    mock_import_module.side_effect = side_effect

    # Testowanie AlgorithmStore
    store = AlgorithmStore()
    ref_alg = store.time_reference_algorithm
    assert isinstance(ref_alg, Algorithm)

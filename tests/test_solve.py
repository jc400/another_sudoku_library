import pytest
from another_sudoku_library.solve import _getRowVals, _getColVals, _getSqrVals, solve
from . import sample_boards


def test_getRowVals():
    assert _getRowVals(sample_boards.t1, 3, 7, inclusive=False) == [6, 5, 7]


def test_getColVals():
    assert _getColVals(sample_boards.t1, 1, 1, inclusive=False) == [2, 4, 5]


def test_getSqrVals():
    assert _getSqrVals(sample_boards.t1, 4, 4, inclusive=False) == [5, 7]


@pytest.mark.parametrize(
    "pz",
    (
        {"problem": sample_boards.t2_problem, "solution": sample_boards.t2_solution},
        {"problem": sample_boards.t3_problem, "solution": sample_boards.t3_solution},
    ),
)
def test_solve_t2(pz):
    assert solve(pz["problem"]) == pz["solution"]

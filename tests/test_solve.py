from another_sudoku_library.solve import _getRowVals, _getColVals, _getSqrVals
from .sample_boards import t5


def test_getRowVals():
    assert _getRowVals(t5, 3, 7, inclusive=False) == [6, 5, 7]


def test_getColVals():
    assert _getColVals(t5, 1, 1, inclusive=False) == [2, 4, 5]


def test_getSqrVals():
    assert _getSqrVals(t5, 4, 4, inclusive=False) == [5, 7]

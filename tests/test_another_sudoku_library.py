#!/usr/bin/env python

"""Tests for `another_sudoku_library` package."""

import pytest


from another_sudoku_library import another_sudoku_library


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


import timeit

def test_rowGen():
    
    # call func, no test data needed
    res = list(rowGen(3, 7, inclusive=False))
    
    # test against hardcoded answer ( a list of y/x tuples)
    if res != [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 8)]:
        print("FAIL. got: ", res)
    else:
        print("passed.")

def test_colGen():
    
    # call func, no test data needed
    res = list(colGen(3, 7, inclusive=False))
    
    # test against hardcoded answer ( a list of y/x tuples)
    if res != [(0, 7), (1, 7), (2, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7)]:
        print("FAIL. got: ", res)
    else:
        print("passed.")

def test_sqrGen():
    
    # call func, no test data needed
    res = list(sqrGen(3, 7, inclusive=False))
    
    # test against hardcoded answer ( a list of y/x tuples)
    if res != [(3, 6), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)]:
        print("FAIL. got: ", res)
    else:
        print("passed.")

def test_fullGen():
    res = list(fullGen())
    expected = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), 
    (0, 7), (0, 8), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
    (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), 
    (2, 7), (2, 8), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), 
    (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), 
    (4, 7), (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), 
    (5, 7), (5, 8), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), 
    (6, 7), (6, 8), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), 
    (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), 
    (8, 7), (8, 8)]
    
    if res != expected:
        print("FAIL. Got: ", res)
    else:
        print("passed.")
    


def test_getRowVals():
    # init testboard
    t5 =  [[0,0,0,0,0,0,0,4,8],
        [0,8,6,9,0,0,0,0,1],
        [0,2,0,0,8,3,7,0,0],
        [6,0,0,5,0,0,0,1,7],
        [0,0,0,0,6,0,4,0,0],
        [2,4,0,0,0,7,0,0,5],
        [0,0,2,3,5,0,0,8,0],
        [3,0,0,0,0,8,5,7,0],
        [9,5,0,0,0,0,0,0,0],]
        
    # call func on test board with args
    res = getRowVals(t5, 3, 7, inclusive=False)
    
    # test against hardcoded answer
    if res != [6, 5, 7]:
        print("FAIL. got: ", res)
    else:
        print("passed.")
        
def test_getColVals():
    # init testboard
    t5 =  [[0,0,0,0,0,0,0,4,8],
        [0,8,6,9,0,0,0,0,1],
        [0,2,0,0,8,3,7,0,0],
        [6,0,0,5,0,0,0,1,7],
        [0,0,0,0,6,0,4,0,0],
        [2,4,0,0,0,7,0,0,5],
        [0,0,2,3,5,0,0,8,0],
        [3,0,0,0,0,8,5,7,0],
        [9,5,0,0,0,0,0,0,0],]
        
    # call func on test board with args
    res = getColVals(t5, 1, 1, inclusive=False)
    
    # test against hardcoded answer
    if res != [2, 4, 5]:
        print("FAIL. got: ", res)
    else:
        print("passed.")

def test_getSqrVals():
    # init testboard
    t5 =  [[0,0,0,0,0,0,0,4,8],
        [0,8,6,9,0,0,0,0,1],
        [0,2,0,0,8,3,7,0,0],
        [6,0,0,5,0,0,0,1,7],
        [0,0,0,0,6,0,4,0,0],
        [2,4,0,0,0,7,0,0,5],
        [0,0,2,3,5,0,0,8,0],
        [3,0,0,0,0,8,5,7,0],
        [9,5,0,0,0,0,0,0,0],]
        
    # call func on test board with args
    res = getSqrVals(t5, 4, 4, inclusive=False)
    
    # test against hardcoded answer
    if res != [5, 7]:
        print("FAIL. got: ", res)
    else:
        print("passed.")


    



def quick(inString):
    return timeit.timeit(stmt=inString, globals=globals(), number=10000)
def slow(inString):
    return timeit.timeit(stmt=inString, globals=globals(), number=500) 
def verySlow(inString):
    return timeit.timeit(stmt=inString, globals=globals(), number=50) 
def superSlow(inString):
    return timeit.timeit(stmt=inString, globals=globals(), number=5)

def speedTests():
    import timeit

    def quick(inString):
        return timeit.timeit(stmt=inString, globals=globals(), number=10000)
    def slow(inString):
        return timeit.timeit(stmt=inString, globals=globals(), number=500) 
    def verySlow(inString):
        return timeit.timeit(stmt=inString, globals=globals(), number=50) 

    print("rowGen()", "---",        quick("rowGen(3,3)"))
    print("colGen()", "---",        quick("colGen(3,3)"))
    print("sqrGen()", "---",        quick("sqrGen(3,3)"))
    print("fullGen()", "---",       quick("fullGen()"))
    print()
    print("getRowVals()", "---",    quick("getRowVals(s3,3,3)"))
    print("getColVals()", "---",    quick("getColVals(s3,3,3)"))
    print("getSqrVals()", "---",    quick("getSqrVals(s3,3,3)"))
    print()
    print("getPoss()", "---",       quick("getPoss(s3,3,3)"))
    print("uniqueCheck()", "---",   quick("uniqueCheck(s3,3,3)"))
    print()
    print("===================================")
    print("generateCache()", "---", slow("generateCache(s3)"))
    print("solve()", "---",         slow("solve(s3)"))
    print("checkConsistent()", "---", slow("checkConsistent(s3)"))
    print()
    print("===================================")
    print("generate()", "---", verySlow("generate()"))
    print("carve()", "---", verySlow("carve(f1)"))
    print()
    print("getPuzzle()", "---", verySlow("getPuzzle()"))

def testGen(genFunc):
    board = getEmptyBoard()
    for y, x in genFunc():
        board[y][x] = 'X'
        printBoard(board)
        print('----------------------')
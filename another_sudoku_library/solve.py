"""Functions to solve a sudoku puzzle, and/or check correctness"""

from .utils import rowGen, colGen, sqrGen, fullGen, getEmptyBoard, copyBoard


# Return list of KNOWN values within a row/sqr/col.         
def _getRowVals(board, y, x, inclusive=True):
    """Returns list of values of already set cells in row"""
    out = []
    for y1, x1 in rowGen(y, x, inclusive=inclusive):
        if board[y1][x1] == 0:
            continue 
        elif type(board[y][x]) == int:
            out.append(board[y1][x1])
        else:
            out += board[y1][x1]
    return out   
    
def _getColVals(board, y, x, inclusive=True):
    """Returns list of values of already set cells in col"""
    out = []
    for y1, x1 in colGen(y, x, inclusive=inclusive):
        if board[y1][x1] == 0:
            continue 
        elif type(board[y][x]) == int:
            out.append(board[y1][x1])
        else:
            out += board[y1][x1]
    return out

def _getSqrVals(board, y, x, inclusive=True):
    """Returns list of values of already set cells in sqr"""
    out = []
    for y1, x1 in sqrGen(y, x, inclusive=inclusive):
        if board[y1][x1] == 0:
            continue 
        elif type(board[y][x]) == int:
            out.append(board[y1][x1])
        else:
            out += board[y1][x1]
    return out

def _getPoss(board, y, x):
    """Returns set of possible values for a cell. Returns single-value set if cell is decided."""
    if board[y][x] != 0:
        return [board[y][x]]

    return ({1,2,3,4,5,6,7,8,9}
            -set(_getRowVals(board, y, x))
            -set(_getColVals(board, y, x))
            -set(_getSqrVals(board, y, x)))

def _countZeros(board):
    """Returns count of zeros (eg carved cells) in a provided board. 
    
    Should work on stringify() board, and also full list board"""
    
    if type(board) == str:
        return board.count('0')
        
    zeros = 0
    for y, x in fullGen():
        if board[y][x] == 0:
            zeros += 1
    return zeros



def _generateCache(board):
    """returns parallel cache board, holding set of possibilities for each cell"""
    out = getEmptyBoard()
    for y, x in fullGen():
        out[y][x] = _getPoss(board, y, x)
    return out
    
def _uniqueCheck(board, y, x, cache=None):
    """Tries to solve cell. Return 1-9 if found, 0 if inconclusive, -1 if no possibilities. 
    
        Looks like this is 16x faster w cache provided. Also if we calc cache here, we're doing a lot of
        work to get possibilities for cells we won't access. 
        
        Works by getting the set of possible values
        for the cell, then comparing with the possible values for every other cell in its row/col/sqr.
    """
    
    #run cheap, naive checks first
    cellPoss = _getPoss(board, y, x)
    if len(cellPoss) == 1:      #if cell has one poss, must be answer
        return cellPoss.pop()
    elif len(cellPoss) == 0:    #if no poss for cell, must be error in board
        return -1

    #if no cache, we do have to generate one
    if cache == None:
        cache = _generateCache(board)

    #compare cell possibilities to unit possibilities. Looking for UNIQUE poss in cell
    if cellPoss - set(_getRowVals(cache, y, x, inclusive=False)):
        return (cellPoss - set(_getRowVals(cache, y, x, inclusive=False))).pop()
    if cellPoss - set(_getColVals(cache, y, x, inclusive=False)):
        return (cellPoss - set(_getColVals(cache, y, x, inclusive=False))).pop()
    if cellPoss - set(_getSqrVals(cache, y, x, inclusive=False)):
        return (cellPoss - set(_getSqrVals(cache, y, x, inclusive=False))).pop()
    
    #if inconclusive, just return nothing
    return 0
            
def solve(board, nest=0):
    """This is best-effort solve. Tries its best, but may return an incomplete or inconsistent 
        board. If error, should have that cell as -1. 
    """
    wb = copyBoard(board)   #pure function--dont change original board arg
    c = _generateCache(wb)
    solved = False
    changed = True

    while not solved and changed:           # iterate over board
        changed = False
        for y, x in fullGen():              # use uniqueCheck() against whole board
            if wb[y][x] == 0:               # but skip already solved cells
                wb[y][x] = _uniqueCheck(wb, y, x, cache=c)
                if wb[y][x] > 0:
                    c = _generateCache(wb)       #regen cache if we hit an answer
                    changed = True              #if solved, raise the flag

        if checkComplete(wb):               #now check if it's finished
            solved = True

    #recurse clause (up to 3 times)
    if not solved and nest < 3:
        lpy, lpx = 0, 0     #lynchpin cell coords. Find cell with most possibilities.
        for y, x in fullGen():
            if len(c[y][x]) > len(c[lpy][lpx]):
                lpy, lpx = y, x

        #now we check EACH possibility for lynchpin, to see if we get a solve
        for value in c[lpy][lpx]:
            testWB = copyBoard(wb)              #testWB is a branch--doesn't change orig state of wb
            testWB[lpy][lpx] = value            #make assumption about lynchpin  
            testWB = solve(testWB, nest=nest+1) #try to solve

            if checkComplete(testWB) and checkConsistent(testWB):
                if not solved:
                    wb = testWB
                    solved = True
                else:                           #if board already solved, means multiple solutions
                    print("Error: recursion uncovered multiple valid solutions")
                    wb[0][0] = 0                #in case of multiple valid solutions, fail the board

    #output the now-solved (maybe incomplete) (and maybe inconsistent) board
    return wb 

def checkComplete(board):
    """Naive check whether each cell has been filled (or if its still 0)"""
    for y, x in fullGen():
        if board[y][x] == 0:
            return False 
    return True
        
def checkConsistent(board):
    """Loop through board. If a cell matches another cell in its unit, its not consistent"""

    #check for -1 first, this automatically means error
    if not checkConsistentCheap(board):
        return False
    
    for y, x in fullGen():
        if board[y][x] == 0:    #ignore unset cells
            continue  

        temp = (  
            _getRowVals(board, y, x, inclusive=False) 
            + _getColVals(board, y, x, inclusive=False)
            + _getSqrVals(board, y, x, inclusive=False)
        )
        if board[y][x] in temp:
            return False

    return True

def checkConsistentCheap(board):
    for y, x in fullGen():
        if board[y][x] == -1:
            return False
    return True

def check(board):
    return checkComplete(board) and checkConsistent(board)
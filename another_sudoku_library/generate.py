import random
from .utils import fullGen, exclusiveGen, getEmptyBoard, copyBoard
from .solve import _generateCache, _uniqueCheck, checkComplete, checkConsistent, solve


def _picker(board, y, x, cache=None):
    #short-circuit, if y/x has val already
    if board[y][x] != 0:    
        return board[y][x]
    
    # cache is optional arg, may need to calc
    if cache == None:       
        cache = _generateCache(board)

    #uniqueCheck returns value, or -1 for error
    slv = _uniqueCheck(board, y, x, cache=cache)
    if slv != 0:      
        return slv
    
    # if no existing val, solve, or error, pick randomly from valid opt    
    else:             
        options = list(cache[y][x])
        return options[random.randint(0, len(options)-1)]

def _generate():
    done = False
    while not done:
        n = getEmptyBoard()
        for y, x in fullGen():          # loop through entire board
            n[y][x] = _picker(n, y, x)   # picker solves cell if possible, otherwise gives random

            if y > 5:                   # heuristic: once board is mostly full
                n = solve(n, nest=4)    # start trying to solve remaining cells
                if checkComplete(n):    
                    break

        if checkConsistent(n):
            done = True
    return n

def _removable(board, y, x, nest=4):
    """ Tests whether board can still be solved without given y/x cell. Returns true/false"""
    test = copyBoard(board)        
    test[y][x] = 0
    test = solve(test, nest=nest)  # test to see if board is still solveable after remove

    if checkComplete(test) and checkConsistent(test):
        return True 
    else:
        return False

def _rm(wb, forbid, ry, rx, nest=4):
    """checks whether a cell is removable or not. If yes, removes it. Returns 1 or 0, if removed.
    
    This is NOT PURE. It changes the wb and forbid lists that are passed to it.
    """
    if wb[ry][rx] == 0 or forbid[ry][rx] == 1: 
        return 0
    if _removable(wb, ry, rx, nest=nest):       # if board solveable after removing this coord
        wb[ry][rx] = 0              # remove that cell and continue
        return 1
    else:
        forbid[ry][rx] = 1          # if test fails, forbid value so we dont retest it
        return 0

def _carve(board, count=60):
    """ Takes a full board, and removes cells so that puzzle is still solveable. Removes up to
    count cells (if it can. In practice, we're removing ~60 cells max right now)
    """
    wb = copyBoard(board)
    forbid = getEmptyBoard()            # if a cell is necessary for solve, save coords 
    removes = 0
    attempts = 0

    # stage one: try removing random coords (up to 50 times
    while removes < count and attempts < 50:  
        attempts += 1
        ry = random.randint(0, 8)  
        rx = random.randint(0, 8)
        if _rm(wb, forbid, ry, rx):      # rm() tries remove, updates wb and forbid, returns t/f
            removes += 1
            
    # stage two: crawl entire board and try remove
    if removes < count:
        for ry, rx in exclusiveGen():
            if _rm(wb, forbid, ry, rx): # nest=1):   # can use nesting to get ~5 extra carves (at time cost)
                removes += 1
                if removes == count:
                    break
                
    #print(removes)
    return wb 

def getPuzzle(diff=40):
    """feed it the number of cells to remove. 60 is hard, 25 is easy"""
    return _carve(_generate(), count=diff)


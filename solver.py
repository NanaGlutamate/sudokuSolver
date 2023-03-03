from typing import List, Dict, Tuple, Set
import copy
# from __future__ import annotations

class Sudoku:
    def __init__(self, puzzle: List[List[int]] = None):
        if puzzle is None:
            return
        self.possible = [[{k for k in range(1, 10)} for j in range(9)] for i in range(9)]
        self.puzzle = [[0 for j in range(9)] for i in range(9)]
        self.single: Set[Tuple[int, int]] = set()
        for ind_i, i in enumerate(puzzle):
            for ind_j, j in enumerate(i):
                if j != 0:
                    self.set(ind_i, ind_j, j)

    def set(self, i: int, j: int, value: int):
        assert(self.puzzle[i][j] == 0)
        self.puzzle[i][j] = value
        self.possible[i][j].clear()
        for ind in range(9):
            self.possible[ind][j].discard(value)
            self.possible[i][ind].discard(value)
            self.check(ind, j)
            self.check(i, ind)
        for ind_i in range(i//3*3, i//3*3+3):
            for ind_j in range(j//3*3, j//3*3+3):
                self.possible[ind_i][ind_j].discard(value)
                self.check(ind_i, ind_j)

    def check(self, i, j):
        if len(self.possible[i][j]) == 1:
            self.single.add((i, j))

    def deduce(self)-> bool:
        if not self.single:
            return False
        i, j = self.single.pop()
        if len(self.possible[i][j]) != 1:
            return False
        self.set(i, j, self.possible[i][j].pop())
        return True

    def solve(self)-> bool:
        while self.deduce():
            pass
        if all(all(j!=0 for j in i) for i in self.puzzle):
            return True
        # check()==False <-> len(self.possible[i][j])==0, therefore no need to test check()
        # if not self.check():
        #     return False
        i, j = self.mostReliable()
        for v in self.possible[i][j]:
            search = self.deepcopy()
            search.set(i, j, v)
            if search.solve():
                self.puzzle = search.puzzle
                self.possible = search.possible
                self.single = search.single
                return True
        return False

    # def check(self)-> bool:
    #     for ind_i, i in enumerate(self.puzzle):
    #         for ind_j, j in enumerate(i):
    #             if len(self.possible[ind_i][ind_j]) == 0 and j == 0:
    #                 return False
    #     return True

    def mostReliable(self)-> Tuple[int, int]:
        minlen = 10
        ind_i, ind_j = 0, 0
        for i in range(9):
            for j in range(9):
                l = len(self.possible[i][j])
                if self.puzzle[i][j] == 0 and l < minlen:
                    minlen, ind_i, ind_j = l, i, j
        return ind_i, ind_j

    def deepcopy(self)-> 'Sudoku':
        tmp = Sudoku()
        tmp.possible = copy.deepcopy(self.possible)
        tmp.puzzle = copy.deepcopy(self.puzzle)
        tmp.single = copy.deepcopy(self.single)
        return tmp

def buildPuzzle(s: str)-> List[List[int]]:
    out: List[List[int]] = []
    tmp: List[int] = []
    s = (c for c in s if not (c in set('-|\n][,')))
    for i in s:
        tmp.append(int(i))
        if len(tmp) == 9:
            out.append(tmp)
            tmp = []
    return out

def printPuzzle(puzzle: List[List[int]]):
    for ind, i in enumerate(puzzle):
        print('|'.join(str(j) for j in i))
        if ind % 3 == 2:
            print('-' * 17)

test = [
    [6,0,0,0,0,2,0,8,3],
    [0,0,4,0,0,5,0,1,6],
    [0,0,3,6,0,8,2,0,0],
    [5,7,0,8,0,0,4,0,0],
    [0,2,0,4,7,1,0,3,0],
    [0,0,8,0,0,0,1,6,0],
    [4,0,0,0,8,0,0,0,1],
    [0,0,0,0,0,0,9,2,0],
    [1,6,0,0,2,0,0,0,0],
]

tests = [
    test,
    buildPuzzle('0' * 81),
    buildPuzzle('820000504040000013500804607060030050000209700004001980490000100000070009050000000'),
    buildPuzzle('420800900003020000005000004000900060002000000170080003840070001500000000000001300'),
]

solver = Sudoku(tests[3])
solver.solve()
printPuzzle(solver.puzzle)
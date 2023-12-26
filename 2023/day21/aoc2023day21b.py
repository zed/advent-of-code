#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/21#part2
- what is the key insight that enabled the solution?
  + the sides are empty, so the fastest path is along the sides of the tile
  + look at the actual puzzle input
  + https://www.reddit.com/media?url=https%3A%2F%2Fpreview.redd.it%2F4fchnarzhm7c1.gif%3Fformat%3Dmp4%26s%3D285dbc36968ae598e2652dde18c64824dc048892
    https://www.reddit.com/r/adventofcode/comments/18njrqf/2023_day_21_a_diamond_in_the_rough/
- what is the longest bug to fix?
- what would have made it less likely?
"""
import os
import datetime as DT
import subprocess
from collections import namedtuple
from itertools import starmap

import matplotlib.pyplot as plt
from icecream import ic
from numpy.polynomial import Polynomial
from rich.traceback import install

ic.configureOutput(prefix=lambda: f"{DT.datetime.now():%T}| ")
install(show_locals=True)


Direction = namedtuple("Direction", "r c")

N, E, S, W = starmap(Direction, [(-1, 0), (0, 1), (1, 0), (0, -1)])

NSTEPS = 26501365
EXACT = 636391426712747
GRID: tuple[str]
GRID_SIZE: int


def plot_dependency(xs, ys):
    p = Polynomial.fit(xs, ys, 2)
    print(p)
    print(p.convert())
    plt.scatter(xs, ys, color="red")
    plt.plot(*p.linspace())
    ic(p(NSTEPS), EXACT)
    P = [*map(round, p.convert())]
    ic(P)
    x = (NSTEPS - GRID_SIZE // 2) // GRID_SIZE
    assert x == 202300
    appro = sum(P[n] * x**n for n in range(2 + 1))
    ic(appro)
    ic(EXACT)
    if appro != EXACT:
        plt.savefig("approx_not_equal_exact.png")
        exit(1)
    return appro


def getanswer(data):
    global GRID, GRID_SIZE
    GRID = tuple(data.splitlines())
    assert len(GRID) == len(GRID[0])  # square
    GRID_SIZE = n = len(GRID)
    assert all(n == len(row) for row in GRID)

    # the sides are all '.'
    assert GRID[0].count(".") == len(GRID[0])
    assert GRID[-1].count(".") == len(GRID[-1])
    assert sum(row[0] == "." and row[-1] == "." for row in GRID) == len(GRID)

    # find starting position
    rS, cS = next(
        (r, c)
        for r, row in enumerate(GRID)
        for c, gp in enumerate(row)
        if gp == "S"
    )
    # it is at the center
    assert rS == cS == n // 2
    if n == 131:  # puzzle input
        # central row & columns are all '.' too (except for S)
        assert GRID[rS].replace("S", ".").count(".") == n
        assert all(row[cS] in "S." for row in GRID)
        # same number of steps to each edge N,S,E,W
        assert (n // 2) * 2 == (n - 1)
        # r=n//2 step_count=0
        # r-1    step_count=1
        # r-2    step_count=2
        # r-n//2 step_count=n//2  # 0-th row (edge)

        # how far can we go if we go without turning? how many tiles?
        year = 2023
        assert NSTEPS // n == year * 100  # full tiles
        assert NSTEPS % n == n // 2  # 0-th tile

        # year*100 tiles each direction up, down, left, right
        # (excluding central tile)

        # if central tile is 0, then we reach the furthest edge of
        # year100 tile after NSTEPS

    # Solve puzzle using brute-force for small number of steps
    # Plot dependency: NSTEPS -> how many garden plots could be reached
    # There is a very good visual fit for square formula but exact values
    # are lacking.
    # Try more points?
    xs = [0, 1, 2]
    ys = []
    # use pypy to make it faster
    with subprocess.Popen(
        ["./count_gardent_plots.py", str(max(xs)), "input.txt"],
        stdout=subprocess.PIPE,
        text=True,
        env=dict(os.environ, PYTHONUNBUFFERED="1"),
    ) as p:
        for i, line in enumerate(p.stdout):
            ys.append(int(line.strip()))
            ic(i, ys[i])
    return plot_dependency(xs, ys)


def main():
    """
    ╰─$ time ./aoc2023day21b.py
    23:00:28| i: 0, ys[i]: 3947
    23:00:34| i: 1, ys[i]: 35153
    23:00:55| i: 2, ys[i]: 97459
    35153.0 + 46756.0·x + 15550.0·x²
    3947.0 + 15656.0·x + 15550.0·x²
    23:00:56| p(NSTEPS): 1.0921112908628533e+19, EXACT: 636391426712747
    23:00:56| P: [3947, 15656, 15550]
    23:00:56| appro: 636391426712747
    23:00:56| EXACT: 636391426712747
    ./aoc2023day21b.py  29.33s user 0.39s system 99% cpu 29.910 total
    """
    assert getanswer(open("input.txt").read().strip()) == EXACT


if __name__ == "__main__":
    main()

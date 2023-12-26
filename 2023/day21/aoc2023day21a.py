#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/21#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
  + only the last garden counts
  + global SEEN had issues
- what would have made it less likely?
"""
import functools
from collections import namedtuple
from itertools import starmap

Direction = namedtuple("Direction", "r c")

N, E, S, W = starmap(Direction, [(-1, 0), (0, 1), (1, 0), (0, -1)])
GRID: tuple[str]


def getanswer(data, nsteps=64):
    global GRID
    g = tuple(data.splitlines())
    nrows = len(g)
    ncols = len(g[0])
    assert all(len(row) == ncols for row in g)  # rectangular
    GRID = (
        ("#" * (ncols + 2),)
        + tuple("#" + row + "#" for row in g)
        + ("#" * (ncols + 2),)
    )
    assert len(GRID) == (nrows + 2)
    assert len(GRID[0]) == (ncols + 2)
    assert all(len(row) == (ncols + 2) for row in GRID)  # rectangular
    s = next(
        (r, c)
        for r, row in enumerate(GRID)
        for c, x in enumerate(row)
        if x == "S"
    )
    #### assert count((6, 5), 1) == 3
    #### assert count(s, 0) == 1
    #### assert count(s, 1) == 2
    #### assert count(s, 2) == 4
    #### assert count(s, 3) == 6
    answer = count(s, nsteps)
    print(answer)
    return answer


def count(start_position, nsteps):
    assert GRID[start_position[0]][start_position[1]] != "#"
    seen = set()

    @functools.cache
    def f(r, c, n):
        if not n:  # no steps left
            seen.add((r, c))  # only the last garden plot counts
        else:
            assert n > 0
            for dir_ in [E, W, N, S]:
                dr = r + dir_.r
                dc = c + dir_.c
                if GRID[dr][dc] != "#":
                    f(dr, dc, n - 1)

    f(*start_position, nsteps)
    ####show(seen, nsteps, "->", len(seen))
    return len(seen)


def show(seen, *args):
    print(*args)
    grid = list(map(list, GRID))
    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            if (r, c) in seen:
                assert GRID[r][c] != "#"
                if GRID[r][c] != "S":
                    grid[r][c] = "O"
                else:
                    grid[r][c] = "V"
    print("\n".join(map("".join, grid)), end="\n\n")


def main():
    test_getanswer()


def test_getanswer():
    for data, nsteps, expected_answer in [
        (
            """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""",
            6,
            16,
        ),
        (open("input.txt").read().strip(), 64, 3841),
    ]:
        assert expected_answer == getanswer(data, nsteps)
        print("\n\n")


if __name__ == "__main__":
    main()

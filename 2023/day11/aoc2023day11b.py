#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/11#part2
- what is the key insight that enabled the solution?
  -> shortest path is Manhattan distance
- what is the longest bug to fix?
- what would have made it less likely?
"""
from collections import deque
from itertools import combinations
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)


def getanswer(data, n):
    print(data, n)
    galaxies = []
    img = data.splitlines()
    row_coord = [-1]
    for r, row in enumerate(img):
        if "#" not in row:  # no galaxy
            row_coord.append(row_coord[-1] + n)
        else:
            row_coord.append(row_coord[-1] + 1)
    imgT = list(zip(*img))
    col_coord = [-1]
    for c, col in enumerate(imgT):
        if "#" not in col:
            col_coord.append(col_coord[-1] + n)
        else:
            col_coord.append(col_coord[-1] + 1)

    galaxies = []
    for r, row in enumerate(img, start=1):
        for c, gal in enumerate(row, start=1):
            if gal == "#":
                galaxies.append((row_coord[r], col_coord[c]))

    answer = sum(shortest_path(a, b) for a, b in all_galaxy_pairs(galaxies))
    print(f"{answer=}")
    return answer


def shortest_path(a, b):
    """Find shortest manhattan path between a and b."""
    assert a != b
    sr, sc = a  # source row/column indices
    dr, dc = b  # destination row/column indices
    return abs(sr - dr) + abs(sc - dc)


def all_galaxy_pairs(galaxies):
    return combinations(galaxies, 2)


def main():
    test_answer()
    aocd.submit(getanswer(aocd.data, 1000_000))


def test_answer():
    for data, n, expected_answer in [
        (
            """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""",
            2,
            374,
        ),
        (
            """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""",
            10,
            1030,
        ),
        (
            """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""",
            100,
            8410,
        ),
    ]:
        assert expected_answer == getanswer(data, n)
        print("\n\n")


if __name__ == "__main__":
    main()

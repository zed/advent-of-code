#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/23#part2
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
from collections import defaultdict, namedtuple
from itertools import starmap

import aocd

from rich.traceback import install

install(show_locals=True)


Index = namedtuple("Index", "r c")
N, E, S, W = starmap(Index, [(-1, 0), (0, 1), (1, 0), (0, -1)])
OPPOSITE = {N: S, E: W, S: N, W: E}


def getanswer(data):
    grid = tuple(data.splitlines())
    nrows = len(grid)
    ncols = len(grid[nrows - 1])
    assert all(len(row) == ncols for row in grid)
    assert nrows == ncols
    assert ncols > 2

    end = Index((nrows - 1), (ncols - 2))  # where the path ends
    answer = 0

    def f(src, past_dir):
        nonlocal answer

        assert grid[src.r][src.c] != "#", "can't be forest"
        for dir_ in [N, E, S, W]:
            if dir_ == OPPOSITE[past_dir]:
                continue  # don't go back
            dest = Index(src.r + dir_.r, src.c + dir_.c)
            if dest.r == nrows:
                answer = max(answer, len(path) - 1)
                print(f"\r{answer: 30d}", end="", flush=True)
                break
            if grid[dest.r][dest.c] != "#" and dest not in path:
                # can't go into forest or already seen
                path.add(dest)
                f(dest, dir_)
                path.discard(dest)

    start = Index(0, 1)
    path = set([start])
    import sys

    # ncols*nrows?
    sys.setrecursionlimit(15000000)
    f(start, S)
    print("\n" + str(answer))
    return answer


def main():
    test_getanswer()
    date = dict(day=23, year=2023)
    aocd.submit(getanswer(aocd.get_data(**date)), part="b", **date)


def test_getanswer():
    for data, expected_answer in [
        (
            """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
""",
            154,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

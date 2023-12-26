#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/16#part2
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import time
from collections import deque, namedtuple
from enum import Enum
from functools import partial
from itertools import starmap, chain
import aocd
from blessings import Terminal
from rich import print

from rich.traceback import install

install(show_locals=True)

Direction = namedtuple("Direction", "r c")
NORTH, EAST, SOUTH, WEST = starmap(
    Direction, [(-1, 0), (0, 1), (1, 0), (0, -1)]
)


class Dir(Direction, Enum):
    NORTH = NORTH
    EAST = EAST
    SOUTH = SOUTH
    WEST = WEST


def getanswer(data):
    grid = tuple(data.splitlines())
    nrows = len(grid)
    ncols = len(grid[0])
    assert all(ncols == len(row) for row in grid)  # rectangular
    answer = max(
        starmap(
            partial(count_energized, grid),
            chain(
                top_row(ncols),
                bottom_row(nrows, ncols),
                left_col(nrows),
                right_col(nrows, ncols),
            ),
        )
    )
    print(answer)
    return answer


def top_row(ncols):
    r = 0
    dir_ = SOUTH  # v
    for c in range(ncols):
        yield (r, c, dir_)


def bottom_row(nrows, ncols):
    r = nrows - 1
    dir_ = NORTH  # ^
    for c in range(ncols):
        yield (r, c, dir_)


def left_col(nrows):
    c = 0
    dir_ = EAST  # >
    for r in range(nrows):
        yield (r, c, dir_)


def right_col(nrows, ncols):
    c = ncols - 1
    dir_ = WEST  # <
    for r in range(nrows):
        yield (r, c, dir_)


def count_energized(grid, r, c, dir_):
    seen = set()
    # bfs
    nrows = len(grid)
    ncols = len(grid[0])
    q = deque([(r, c, dir_)])
    while q:
        r, c, dir_ = beam = q.popleft()
        if not (0 <= r < nrows and 0 <= c < ncols):
            continue  # out of bounds
        if beam in seen:  # already seen
            continue  # explore next beam in the queue
        seen.add(beam)
        # show(seen, grid, term)
        # .  - same direction
        # -| - as empty space if "pointy"
        # /\ - 90 degrees
        # otherwise split in 2 beams in "pointy" directions
        go = lambda dir_: q.append((r + dir_.r, c + dir_.c, dir_))
        match grid[r][c]:
            case "-" if dir_ in (NORTH, SOUTH):  # split
                go(EAST)
                go(WEST)
            case "|" if dir_ in (EAST, WEST):  # split
                go(NORTH)
                go(SOUTH)
            case ".":
                go(dir_)  # keep going in the same direction
            case "-" if dir_ in (EAST, WEST):
                go(dir_)  # pass through (same direction)
            case "|" if dir_ in (NORTH, SOUTH):
                go(dir_)  # pass through (same direction)
            case "/":  # reflect
                match dir_:
                    case Dir.EAST:
                        go(NORTH)
                    case Dir.NORTH:
                        go(EAST)
                    case Dir.WEST:
                        go(SOUTH)
                    case Dir.SOUTH:
                        go(WEST)
            case "\\":  # reflect
                match dir_:
                    case Dir.NORTH:
                        go(WEST)
                    case Dir.EAST:
                        go(SOUTH)
                    case Dir.SOUTH:
                        go(EAST)
                    case Dir.WEST:
                        go(NORTH)
    return sum(
        any(
            (r, c, dir_) in seen for dir_ in [NORTH, EAST, SOUTH, WEST]
        )  # energized
        for r in range(nrows)
        for c in range(ncols)
    )


def show(seen, grid, term):
    a = draw(seen, grid)
    with term.location(0, 10):
        print("\n".join(map("".join, a)), end="\n\n")


def draw(seen, grid) -> list[list[str]]:
    a = list(map(list, grid))
    for r, row in enumerate(a):
        for c, tile in enumerate(row):
            if tile != ".":
                continue
            n = sum(
                (r, c, dir_) in seen for dir_ in [NORTH, EAST, SOUTH, WEST]
            )
            if n > 1:
                row[c] = str(n)
            elif n == 0:
                pass
            else:
                assert n == 1
                if (r, c, NORTH) in seen:
                    row[c] = "^"
                elif (r, c, EAST) in seen:
                    row[c] = ">"
                elif (r, c, SOUTH) in seen:
                    row[c] = "v"
                else:
                    assert (r, c, WEST) in seen
                    row[c] = "<"
    return a


def main():
    test_getanswer()
    answer = getanswer(aocd.data)
    assert answer == 8314


def test_getanswer():
    for data, expected_answer in [
        (
            r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""",
            51,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

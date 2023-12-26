#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/16#part1
- what is the key insight that enabled the solution?
  -> the bug was fixed thanks to the visualization
- what is the longest bug to fix?
  + W directions was wrong
  + the first step before while q loop was wrong
- what would have made it less likely?
  + typos, mistakes happen -> the granularity, debugging was
    adequate as is.
"""
import time
from collections import deque, namedtuple
from itertools import starmap
import aocd
from blessings import Terminal
from rich import print

from rich.traceback import install

install(show_locals=True)

Direction = namedtuple("Direction", "r c")
N, E, S, W = starmap(Direction, [(-1, 0), (0, 1), (1, 0), (0, -1)])


def getanswer(data):
    grid = tuple(data.splitlines())
    nrows = len(grid)
    ncols = len(grid[0])
    assert all(ncols == len(row) for row in grid)  # rectangular

    # bfs
    # start at 0,0 move East
    seen = set()
    q = deque([(0, 0, E)])
    term = Terminal()
    while q:
        r, c, dir_ = beam = q.popleft()
        if not (0 <= r < nrows and 0 <= c < ncols):
            continue  # out of bounds
        if beam in seen:  # already seen
            continue  # explore next beam in the queue
        seen.add((r, c, dir_))
        # show(seen, grid, term)
        # .  - same direction
        # -| - as empty space if "pointy"
        # /\ - 90 degrees
        # otherwise split in 2 beams in "pointy" directions
        tile = grid[r][c]
        if (
            tile == "."
            or (tile == "-" and dir_ in (E, W))
            or (tile == "|" and dir_ in (N, S))
        ):
            # same direction
            q.append((r + dir_.r, c + dir_.c, dir_))
        elif tile == "-" and dir_ in (N, S):
            q.append((r + E.r, c + E.c, E))
            q.append((r + W.r, c + W.c, W))
        elif tile == "|" and dir_ in (E, W):
            q.append((r + N.r, c + N.c, N))
            q.append((r + S.r, c + S.c, S))
        else:
            assert tile in "/\\"
            if tile == "/":  # mirror
                if dir_ == E:
                    dir_ = N
                elif dir_ == N:
                    dir_ = E
                elif dir_ == W:
                    dir_ = S
                else:
                    assert dir_ == S
                    dir_ = W
            elif tile == "\\":  # mirror
                if dir_ == N:
                    dir_ = W
                elif dir_ == E:
                    dir_ = S
                elif dir_ == S:
                    dir_ = E
                else:
                    assert dir_ == W
                    dir_ = N
            q.append((r + dir_.r, c + dir_.c, dir_))
    show(seen, grid, term)
    answer = sum(
        any((r, c, dir_) in seen for dir_ in [N, E, S, W])  # energized
        for r in range(nrows)
        for c in range(ncols)
    )
    print(answer)
    return answer


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
            n = sum((r, c, dir_) in seen for dir_ in [N, E, S, W])
            if n > 1:
                row[c] = str(n)
            elif n == 0:
                pass
            else:
                assert n == 1
                if (r, c, N) in seen:
                    row[c] = "^"
                elif (r, c, E) in seen:
                    row[c] = ">"
                elif (r, c, S) in seen:
                    row[c] = "v"
                else:
                    assert (r, c, W) in seen
                    row[c] = "<"
    return a


def main():
    test_getanswer()
    ###aocd.submit(getanswer(aocd.data))


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
            46,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

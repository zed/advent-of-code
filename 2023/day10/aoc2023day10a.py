#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/10#part1
"""
from collections import deque
import aocd
from rich import print


def getanswer(data):
    # surround with ground in all directions
    lines = data.splitlines()
    N = len(lines[0])
    assert all(len(row) == len(lines[0]) for row in lines)
    a = [list("." * (N + 2))]
    a += [list("." + row + ".") for row in lines]
    a += [list("." * (N + 2))]

    # find S
    i, j = next(
        (i, j)
        for i, row in enumerate(a)
        for j, c in enumerate(row)
        if c == "S"
    )
    q = deque([(i, j, 0)])
    while q:
        i, j, n = q.popleft()
        a[i][j] = n
        # find pipes connected to (i,j)
        if a[i - 1][j] in ["|", "7", "F"]:  # ^ north
            q.append((i - 1, j, n + 1))
        if a[i + 1][j] in ["|", "L", "J"]:  # V south
            q.append((i + 1, j, n + 1))
        if a[i][j + 1] in ["-", "J", "7"]:  # > east
            q.append((i, j + 1, n + 1))
        if a[i][j - 1] in ["-", "L", "F"]:  # < west
            q.append((i, j - 1, n + 1))
    return max(n for row in a for n in row if isinstance(n, int))


def main():
    data = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""
    data = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
    data = aocd.data
    print(data)
    answer = getanswer(data)
    print(answer)
    ###aocd.submit(answer)


if __name__ == "__main__":
    main()

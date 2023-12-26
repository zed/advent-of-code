#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/11#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
  -> stuck on the idea of optimization (ignoring that
  finding Manhattan distance is trivial)
- what would have made it less likely?
"""
from collections import deque
from itertools import combinations
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)


def getanswer(data):
    print(data)
    # expand rows
    img = []
    for row in data.splitlines():
        img.append(row)
        if row.count(".") == len(row):
            img.append(row)
    # expand  columns
    timg = []  # transposed image
    for col in zip(*img):
        timg.append(col)
        if col.count(".") == len(col):
            timg.append(col)
    # transpose back
    img = list(zip(*timg))
    # XXX use dynamic programmming (cache shorttest paths?)
    answer = sum(shortest_path(a, b, img) for a, b in all_galaxy_pairs(img))
    print(f"{answer=}")
    return answer


def shortest_path(a, b, img):
    """Find shortest manhattan path between a and b in img."""
    dr, dc = b
    q = deque([(a, 0)])
    seen = {}
    while q:
        (
            sr,
            sc,
        ), dist = q.popleft()  # source row/column indices, distance from a
        if sr == dr and sc == dc:
            # found path
            return dist

        # try all 4 directions
        # up
        if (sr - dr) > 0 and sr > 0:
            nr = sr - 1
            if (nr, sc) not in seen:
                seen[nr, sc] = True
                q.append(((nr, sc), dist + 1))
        # down
        if (sr - dr) < 0 and sr < (len(img) - 1):
            nr = sr + 1
            if (nr, sc) not in seen:
                seen[nr, sc] = True
                q.append(((nr, sc), dist + 1))
        # left
        if (sc - dc) > 0 and sc > 0:
            nc = sc - 1
            if (sr, nc) not in seen:
                seen[sr, nc] = True
                q.append(((sr, nc), dist + 1))
        # right
        if (sc - dc) < 0 and sc < (len(img[sr]) - 1):
            nc = sc + 1
            if (sr, nc) not in seen:
                seen[sr, nc] = True
                q.append(((sr, nc), dist + 1))
    assert 0, "can't happen"


def all_galaxy_pairs(img):
    gals = [
        (r, c)
        for r, row in enumerate(img)
        for c, gal in enumerate(row)
        if gal == "#"
    ]
    return combinations(gals, 2)


def main():
    test_answer()
    aocd.submit(getanswer(aocd.data))


def test_answer():
    for data, expected_answer in [
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
            374,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

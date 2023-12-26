#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/17#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import math
from collections import deque, namedtuple
from itertools import starmap
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)
Direction = namedtuple("Direction", "r c")
N, E, S, W = starmap(Direction, [(-1, 0), (0, 1), (1, 0), (0, -1)])


def getanswer(data):
    grid = tuple(tuple(map(int, row)) for row in data.splitlines())
    nrows = len(grid)
    ncols = len(grid[0])
    assert all(ncols == len(row) for row in grid)
    # lava pool to machine parts factory
    # minimize heat loss
    #  straight line for too long.
    sr, sc = 0, 0
    # no heat loss on start!
    MAX_STRAIGHT = 3  # at most for single direction
    # 90 left right
    endr, endc = nrows - 1, ncols - 1
    loss = [[math.inf] * ncols for _ in range(nrows)]
    loss[sr][sc] = 0
    path_east = (sr + E.r, sc + E.c, (None, None, E))
    path_south = (sr + S.r, sc + S.c, (None, None, S))
    q = deque(
        [
            path_east,
            path_south,
        ]
    )
    path_loss = {}  # path -> loss
    path_loss[path_east] = loss[sr][sc] + grid[sr + E.r][sc + E.c]
    path_loss[path_south] = loss[sr][sc] + grid[sr + S.r][sc + S.c]
    while q:
        src_path = q.popleft()  # bfs
        sr, sc, dirs = src_path

        def go(dir_):
            dr, dc = sr + dir_.r, sc + dir_.c
            path = (dr, dc, (dirs[-2], dirs[-1], dir_))
            loss = path_loss[src_path] + grid[dr][dc]
            if loss >= path_loss.get(path, math.inf):
                # already seen path with max history that is not worse
                return
            path_loss[path] = loss
            q.append(path)

        # N
        if sr > 0 and dirs.count(N) < MAX_STRAIGHT and dirs[-1] != S:
            go(N)
        # E
        if sc < (ncols - 1) and dirs.count(E) < MAX_STRAIGHT and dirs[-1] != W:
            go(E)
        # S
        if sr < (nrows - 1) and dirs.count(S) < MAX_STRAIGHT and dirs[-1] != N:
            go(S)
        # W
        if sc > 0 and dirs.count(W) < MAX_STRAIGHT and dirs[-1] != E:
            go(W)
    answer = min(
        loss
        for (r, c, _), loss in path_loss.items()
        if r == endr and c == endc
    )
    print(answer)
    return answer


def main():
    test_getanswer()
    aocd.submit(getanswer(aocd.data))


def test_getanswer():
    for data, expected_answer in [
        (
            """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""",
            102,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

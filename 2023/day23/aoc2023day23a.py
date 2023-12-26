#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/23#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import time
from collections import defaultdict, namedtuple
from enum import Enum
from itertools import starmap

import aocd
from blessed import Terminal

Index = namedtuple("Index", "r c")
N, E, S, W = starmap(Index, [(-1, 0), (0, 1), (1, 0), (0, -1)])


class Dir(Index, Enum):
    N = N
    E = E
    S = S
    W = W


def getanswer(data):
    grid = tuple(data.splitlines())
    nrows = len(grid)
    ncols = len(grid[nrows - 1])
    assert all(len(row) == ncols for row in grid)
    assert nrows == ncols
    assert ncols > 2
    src = start = Index(0, 1)
    end = Index((nrows - 1), (ncols - 2))
    # longest hike
    # manhatten
    # NP-hard https://en.wikipedia.org/wiki/Longest_path_problem
    # linear for DAG -> there are cycles -> dead end
    opposite = {N: S, E: W, S: N, W: E}
    seen = set([start])
    dest = Index(
        start.r + S.r, start.c + S.c
    )  # make the step manually to get rid of
    # `if 0 <= dest.r < nrows and 0 <= dest.c < ncols` condition

    # hints:
    # Do a DFS on the tree and record finishing times
    # Sort vertexes by finishing time (aka topo-sort)
    # Relax outgoing edges of vertexes in order of finishing times with negated edge weights
    # let's dp be longest Directed Path from src
    ldp = defaultdict(int)
    path = 1  # path id
    ldp[dest, path] = max(ldp[dest, path], 1 + ldp[src, path])
    seen.add((dest, path))
    q = [(dest, S, path)]  # dfs
    term = Terminal()
    w = lambda y, x, s: print(
        term.move_yx(y + 1, x) + str(s), end="", flush=True
    )
    with term.cbreak(), term.hidden_cursor():
        for r, row in enumerate(grid):
            w(r, 0, row)
        while q:
            src, past_dir, path = q.pop()
            assert (src, path) in seen

            def try_go(dir_):
                if dir_ == opposite[past_dir]:
                    return  # don't go back
                dest = Index(src.r + dir_.r, src.c + dir_.c)
                if dir_ == S and dest.r == nrows:
                    return  # outside maze
                if grid[dest.r][dest.c] != "#" and (dest, path) not in seen:
                    # can't go into forest or already seen
                    match dir_:
                        case Dir.N | Dir.S:
                            c = "|"
                        case Dir.E | Dir.W:
                            c = "-"
                    w(*src, c)
                    return dest, dir_

            went = []
            match grid[src.r][src.c]:
                case "#":
                    assert 0, "can't be forest"
                case "^":
                    went.append(try_go(N))
                case ">":
                    went.append(try_go(E))
                case "v":
                    went.append(try_go(S))
                case "<":
                    went.append(try_go(W))
                case ".":
                    for option, dir_ in enumerate([N, E, S, W]):
                        went.append(try_go(dir_))
            if went:
                if len(went) == 1 and went[0]:
                    [(dest, dir_)] = went
                    seen.add((dest, path))
                    q.append((dest, dir_, path))
                    ldp[dest, path] = max(ldp[dest, path], 1 + ldp[src, path])
                    w(*dest, path)
                    w(nrows, ncols, ldp[dest, path])
                else:
                    went = list(filter(None, went))[::-1]
                    for new_path, (dest, dir_) in enumerate(
                        went, start=path + 1
                    ):
                        seen.add((dest, new_path))
                        q.append((dest, dir_, new_path))
                        ldp[dest, new_path] = max(
                            ldp[dest, path], 1 + ldp[src, path]
                        )
                        w(
                            *dest,
                            max(
                                (L for (p, _), L in ldp.items() if p == end),
                                default=0,
                            )
                        )
                        w(nrows, 0, ldp[dest, new_path])

                        w(nrows, ncols, ldp[dest, new_path])

    answer = max(L for (p, _), L in ldp.items() if p == end)
    print(answer)
    return answer


def main():
    test_getanswer()
    aocd.submit(getanswer(aocd.data))


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
            94,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/10#part2

Key insights:
- ray tracing doesn't work on the boundary -> polygon.contains()
- there may be more than 2 pipes connected -> G.find_cycle()
"""
from itertools import repeat, count
import aocd
import networkx as nx
from rich import print

from rich.traceback import install

install(show_locals=True)

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def getanswer(data):
    # surround with ground in all directions
    lines = data.splitlines()
    N = len(lines[0])
    assert all(len(row) == len(lines[0]) for row in lines)
    a = [list("." * (N + 2))]
    a += [list("." + row + ".") for row in lines]
    a += [list("." * (N + 2))]
    print("\n".join(["".join([str(c).rjust(2) for c in row]) for row in a]))

    # find S
    i, j = start_node = next(
        (i, j)
        for i, row in enumerate(a)
        for j, c in enumerate(row)
        if c == "S"
    )
    # find main loop
    q = [(i, j, 0)]
    G = nx.Graph()
    while q:
        # XXX check puzzle description for the condition on 2 pipes
        # for the start node
        # XXX check for allowed direction the _starting_ node too!
        i, j, n = q.pop()
        a[i][j] = n
        # find pipes connected to (i,j)
        if a[i - 1][j] in ["|", "7", "F"]:  # ^ north
            q.append((i - 1, j, n + 1))
            G.add_edge((i, j), (i - 1, j))
        if a[i + 1][j] in ["|", "L", "J"]:  # V south
            q.append((i + 1, j, n + 1))
            G.add_edge((i, j), (i + 1, j))
        if a[i][j + 1] in ["-", "J", "7"]:  # > east
            q.append((i, j + 1, n + 1))
            G.add_edge((i, j), (i, j + 1))
        if a[i][j - 1] in ["-", "L", "F"]:  # < west
            q.append((i, j - 1, n + 1))
            G.add_edge((i, j), (i, j - 1))
    # XXX there should be no need for find_cycle with correct condition on allowed direction (just use bfs [deque])
    points = [edge[0] for edge in nx.find_cycle(G, source=start_node)]
    # XXX implement using ray casting
    polygon = Polygon(points)
    answer = sum(
        map(
            polygon.contains,
            [Point(i, j) for i, row in enumerate(a) for j in range(len(row))],
        )
    )
    print(answer)
    return answer


def main():
    test_answer()
    aocd.submit(getanswer(aocd.data))


def test_answer():
    for data, expected_answer in [
        (
            """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""",
            4,
        ),
        (
            """\
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
""".replace(
                "I", "."
            ).replace(
                "O", "."
            ),
            4,
        ),
        (
            """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""",
            8,
        ),
        (
            """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""",
            10,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

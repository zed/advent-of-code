#!/usr/bin/env python
"""https://adventofcode.com/2023/day/22#part2
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
  -> would_collide_xy() (swapped min/max)
  -> mark occupied after the fall didn't handle bricks aligned
     vertically (height > 1 along z)
- what would have made it less likely?
  -> testing

"""
import copy
from collections import defaultdict, deque
from itertools import groupby, pairwise
from dataclasses import dataclass, fields
from typing import NamedTuple

import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)


def field_names(data):
    return [f.name for f in fields(data)]


@dataclass
class MutablePoint:
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int


assert field_names(MutablePoint) == field_names(Point)


class MutableBrick(NamedTuple):
    a: MutablePoint
    b: MutablePoint


class Brick(NamedTuple):
    a: Point
    b: Point


assert MutableBrick._fields == Brick._fields


def data_values(data):
    return (getattr(data, f.name) for f in fields(data))


def lowest_point(brick: MutableBrick) -> int:
    """Lowest point z-coord of the *brick*."""
    assert brick.a.z <= brick.b.z
    return brick.a.z


def parse_data(data: str) -> list[MutableBrick]:
    vert = lambda p: (p.z, p.x, p.y)

    bricks = []
    for position in data.splitlines():
        a, sep, b = position.partition("~")
        assert sep == "~"
        to_point = lambda s: MutablePoint(*map(int, s.split(",")))
        # a point is not higher than b
        a, b = sorted(map(to_point, [a, b]), key=vert)
        assert a.z <= b.z
        # all coords are non-negative
        assert all(c >= 0 for p in [a, b] for c in data_values(p))
        # there is a projection where it is just one cube
        assert (
            sum(ca == cb for ca, cb in zip(data_values(a), data_values(b)))
            >= 2
        )
        bricks.append(MutableBrick(a, b))

    bricks.sort(key=lowest_point)
    return bricks


def settle_bricks(bricks: list[MutableBrick]) -> list[Brick]:
    """Let bricks fall on each other (and the ground)."""
    # find ground support
    minx, miny, maxx, maxy, minz, maxz = 0, 0, 0, 0, 0, 0
    for br in bricks:
        for p in br:
            minx = min(minx, p.x)
            miny = min(miny, p.y)
            maxx = max(maxx, p.x)
            maxy = max(maxy, p.y)
            maxz = max(maxz, p.z)
            assert minz < p.z <= maxz
    # whether occupied? [z][y][x]
    o = [
        [[None] * (maxx - minx + 1) for _ in range(maxy - miny + 1)]
        for _ in range(maxz - minz + 1)
    ]
    # ground is occupied
    for row in o[0]:
        for c in range(len(row)):
            row[c] = True
    #
    for lpz, same_lp_bricks in groupby(bricks, key=lowest_point):
        for br in same_lp_bricks:
            a, b = br
            assert lpz == a.z <= b.z
            assert a.x <= b.x

            for z_occupied in range(lpz - 1, -1, -1):
                # if any occupied
                if any(
                    o[z_occupied][y][x]
                    for y in range(min(a.y, b.y), max(a.y, b.y) + 1)
                    for x in range(min(a.x, b.x), max(a.x, b.x) + 1)
                ):
                    break
            else:
                assert 0, "can't be: there is a ground at the very least"

            # move brick down
            diff = b.z - a.z
            assert a.z > z_occupied
            h = a.z - z_occupied - 1  # drop height
            a.z -= h
            b.z -= h
            assert br.a.z == (z_occupied + 1)
            assert diff == (b.z - a.z)

            # mark occupied after the fall
            for y in range(min(a.y, b.y), max(a.y, b.y) + 1):
                for x in range(min(a.x, b.x), max(a.x, b.x) + 1):
                    for z in range(z_occupied, b.z):
                        assert o[z + 1][y][x] is None  # was unoccupied
                        # Two bricks cannot occupy the same position, so a falling brick
                        # will come to rest upon the first other brick it encounters
                        o[z + 1][y][x] = True

    bricks.sort(key=lowest_point)
    bricks = [
        Brick(Point(*data_values(br.a)), Point(*data_values(br.b)))
        for br in bricks
    ]
    if len(bricks) > 10:
        assert bricks[-1].a.z == 175
    return bricks


def would_collide_xy(b1: Brick, b2: Brick) -> bool:
    """Whether bricks would collide in xy plain (ignoring z)."""
    # ( [ ) ]
    # 0 1 2 3
    assert b1.a.x <= b1.b.x
    assert b2.a.x <= b2.b.x
    assert b1.a.y <= b1.b.y
    assert b2.a.y <= b2.b.y
    return max(b1.a.x, b2.a.x) <= min(b1.b.x, b2.b.x) and max(
        b1.a.y, b2.a.y
    ) <= min(b1.b.y, b2.b.y)


def find_supporters(bricks) -> dict[Brick, set[Brick]]:
    """Brick -> bricks it lies on: top -> bottoms."""
    supporters = defaultdict(set)
    # find what supports what in O(n**2)
    for top in bricks:
        assert 0 < top.a.z <= top.b.z
        for bottom in bricks:
            # highest point of bottom brick is the same as lowest point of the top brick
            if (bottom.b.z + 1) == top.a.z and would_collide_xy(top, bottom):
                supporters[top].add(bottom)
    return dict(supporters)


def find_supported(bricks, supporters) -> dict[Brick, set[Brick]]:
    """Brick -> bricks lying on top of it: bottom -> tops."""
    supported = defaultdict(set)
    # O(n**2)
    for top in bricks:
        for bottom in supporters.get(top, []):
            supported[bottom].add(top)
    return dict(supported)


def getanswer(data: str):
    bricks = settle_bricks(parse_data(data))
    assert sorted(bricks, key=lowest_point) == bricks
    supporters = find_supporters(bricks)  # top -> bottoms
    supported = find_supported(bricks, supporters)

    # sanity check
    names = {brick: name for name, brick in zip("ABCDEFGH", bricks)}

    # count _other_ falling bricks if disintegrate current one
    answer = 0
    for disintegrated in bricks:
        name = names.get(disintegrated)  # a few names for debugging
        # how many _other_ bricks would fall if a brick disintegrated (cascade)
        q = deque([disintegrated])
        nonholding_bricks = set(q)  # either disintegrated or falling
        while q:
            # Settled bricks:
            #
            # 012 x    012 y
            # ---ground---
            # .a. 1 z  aaa
            # ??? 2 z  b.c
            # d.e 3 z  ???
            # fff 4 z  .f.
            # .g. 5 z  .g.
            # .g. 6 z  .g.
            #
            nonholding = q.popleft()
            # find bricks that were supported by the *nonholding* brick
            if nonholding in supported:
                # remove bricks we already know that are nonholding
                for top in supported[nonholding] - nonholding_bricks:
                    if supporters[top] <= nonholding_bricks:  # no support left
                        nonholding_bricks.add(top)  # it is also nonholding
                        q.append(top)  # check for cascade effect

        # don't count disintegrated brick itself
        count = len(nonholding_bricks) - 1
        if name:
            print(name, count)

        answer += count
    print(answer)
    assert answer in (7, 96356)
    return answer


def main():
    test_getanswer()


def test_getanswer():
    for data, expected_answer in [
        (
            """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""",
            7,
        ),
        (open("input.txt").read().strip(), 96356),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

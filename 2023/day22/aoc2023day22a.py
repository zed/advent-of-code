#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/22#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import copy
from itertools import groupby, pairwise
from dataclasses import dataclass, fields


@dataclass
class Point:
    x: int
    y: int
    z: int


def data_values(data):
    return (getattr(data, f.name) for f in fields(data))


def getanswer(data):
    vert = lambda p: (p.z, p.x, p.y)
    lowest_point = lambda br: br[0].z

    bricks = []
    for position in data.splitlines():
        a, sep, b = position.partition("~")
        assert sep == "~"
        to_point = lambda s: Point(*map(int, s.split(",")))
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
        bricks.append((a, b))
    bricks.sort(key=lowest_point)

    # make each brick one cube height
    short_bricks = []
    for br in bricks:
        a, b = br
        for z in range(a.z, b.z + 1):
            short_bricks.append((Point(a.x, a.y, z), Point(b.x, b.y, z)))
    bricks = short_bricks

    # find ground support
    minx, miny, maxx, maxy, minz, maxz = 0, 0, 0, 0, 0, bricks[-1][-1].z
    for br in bricks:
        for p in br:
            minx = min(minx, p.x)
            miny = min(miny, p.y)
            maxx = max(maxx, p.x)
            maxy = max(maxy, p.y)
            assert minz < p.z <= maxz
    # support[z][y][x]
    o = [
        [[None] * (maxx - minx + 1) for _ in range(maxy - miny + 1)]
        for _ in range(maxz - minz + 1)
    ]
    # ground is occupied
    for row in o[0]:
        for c in range(len(row)):
            row[c] = True
    for lpz, same_lp_bricks in groupby(bricks, key=lowest_point):
        for br in same_lp_bricks:
            a, b = br
            assert lpz == a.z <= b.z
            assert a.x <= b.x

            for z in range(lpz - 1, -1, -1):
                # if any occupied
                if any(
                    o[z][y][x]
                    for y in range(min(a.y, b.y), max(a.y, b.y) + 1)
                    for x in range(a.x, b.x + 1)
                ):
                    break
            else:
                assert 0, "can't be: there is a ground at the very least"

            # mark occupied
            for y in range(min(a.y, b.y), max(a.y, b.y) + 1):
                for x in range(a.x, b.x + 1):
                    assert o[z + 1][y][x] is None  # was unoccupied
                    # Two bricks cannot occupy the same position, so a falling brick
                    # will come to rest upon the first other brick it encounters
                    o[z + 1][y][x] = True

            # move brick down
            diff = b.z - a.z
            old, a.z = a.z, (z + 1)
            assert br[0].z == (z + 1)
            b.z -= old - a.z
            assert diff == (b.z - a.z)

    bricks.sort(key=lowest_point)

    # brute force works 45_000_000
    count = 0  # count bricks that can be removed without falling any above
    for same_lp_bricks, same_lp_bricks_next in pairwise(
        (tuple(g) for _, g in groupby(bricks, key=lowest_point))
    ):
        minx, miny, maxx, maxy = [0] * 4
        for br in same_lp_bricks:
            for p in br:
                minx = min(minx, p.x)
                miny = min(miny, p.y)
                maxx = max(maxx, p.x)
                maxy = max(maxy, p.y)
        # occupied? o[y][x]
        o = [[None] * (maxx - minx + 1) for _ in range(maxy - miny + 1)]
        for br in same_lp_bricks:
            a, b = br
            # mark occupied
            for y in range(min(a.y, b.y), max(a.y, b.y) + 1):
                for x in range(a.x, b.x + 1):
                    assert o[y][x] is None  # was unoccupied
                    # Two bricks cannot occupy the same position, so a falling brick
                    # will come to rest upon the first other brick it encounters
                    o[y][x] = True

        # will any (lpz + 1) bricks fall if br is removed?
        old = o
        for br in same_lp_bricks:
            a, b = br
            # mark unoccupied
            o = copy.deepcopy(old)
            for y in range(min(a.y, b.y), max(a.y, b.y) + 1):
                for x in range(a.x, b.x + 1):
                    o[y][x] = None  # mark unoccupied (as if br is removed)
            for br_next in same_lp_bricks_next:
                a_next, b_next = br_next
                # can fall?
                if all(
                    y >= len(o) or x >= len(o[y]) or o[y][x] is None
                    for y in range(
                        min(a_next.y, b_next.y), max(a_next.y, b_next.y) + 1
                    )
                    for x in range(a_next.x, b_next.x + 1)
                ):
                    break
            else:  # no break: none can fall
                count += 1

    count += len(same_lp_bricks_next)  # top-most bricks can be removed freely
    # x:
    #   012
    #   ---
    # 1  #
    # 2 ###
    #   01
    # 0 AA
    # a == b means 1 cube i.e., coordinates inclusive brick on the
    # ground has z=1 coordinate! (ground is z=0)

    # TODO display projections like in the description

    # brick can be safely disintegrated if,
    # after removing it,
    # no other bricks would fall further directly downward.
    answer = count
    print(answer)
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
            5,
        ),
        (open("input.txt").read().strip(), 490),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

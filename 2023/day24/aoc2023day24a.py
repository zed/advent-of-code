#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/24#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
  -> shouldn't have tried to solve it manually
- what would have made it less likely?
  ->  don't do computers job: just use sympy for such algebraic manipulations
"""
import math
from typing import NamedTuple
from itertools import combinations
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)


class Point(NamedTuple):
    x: int
    y: int
    z: int


def to_point(text):
    return Point(*map(int, text.split(",")))


def getanswer(data, min_, max_):
    ###data = open("input.txt").read().strip()
    # parse input
    heil = []
    for line in data.splitlines():
        position_data, sep, velocity_data = line.partition(" @ ")
        assert sep
        position, velocity = map(to_point, [position_data, velocity_data])
        heil.append((position, velocity))
    # one nanosecond
    # forward in time
    # intersections between the paths they will trace within [min_, max_]
    # ignore Z
    # 300 -> even n**4 is ok

    # for all ~50k pairs
    answer = 0
    for a, b in combinations(heil, r=2):
        intesected = False

        # find out whether a, b heils path will cross inside test area
        [(ax0, ay0, _), (avx, avy, _)] = a
        [(bx0, by0, _), (bvx, bvy, _)] = b
        assert bvx + bvy
        assert avx + avy

        # x(t) = x(0) + vx*t
        # y(t) = y(0) + vy*t
        xmin, xmax, ymin, ymax = min_, max_, min_, max_
        #
        # intersection:
        # xmin <= ax(t1) = bx(t2) <= xmax
        # ymin <= ay(t1) = by(t2) <= ymax
        # t1 >= 0, t2 >= 0
        # lines: parallel, intersect future within test area, intersect in the past, intersect outside test area
        # ax0 + avx*t1 = bx0 + bvx*t2
        # ay0 + avy*t1 = by0 + bvy*t2
        #

        """
        Manually:
        ax0+ay0+(avx+avy)*t1 = bx0+by0+(bvx+bvy)*t2
        (bvx+bvy)*t2 = ax0+ay0+(avx+avy)*t1 - bx0 - by0
        t2 = (ax0+ay0+(avx+avy)*t1 - bx0 - by0) / (bvx+bvy)
        t1 = (bx0+by0+(bvx+bvy)*t2 - ax0 - ay0) / (avx+avy)

        # in t1
        ax0+ay0+(avx+avy)*t1 = bx0+by0+(bvx+bvy)*((ax0+ay0+(avx+avy)*t1 - bx0 - by0) / (bvx+bvy))
        (bvx+bvy)*(ax0+ay0+(avx+avy)*t1) = bx0+by0+(bvx+bvy)*((ax0+ay0+(avx+avy)*t1 - bx0 - by0))

        bvx*(ax0+ay0+(avx+avy)*t1) + bvy*(ax0+ay0+(avx+avy)*t1) =
        = bx0+by0+ bvx*((ax0+ay0+(avx+avy)*t1 - bx0 - by0)) + bvy*((ax0+ay0+(avx+avy)*t1 - bx0 - by0))

        bvx*(ax0+ay0)+bvx*(avx+avy)*t1 + bvy*(ax0+ay0)+bvy*(avx+avy)*t1 =
        = bx0+by0+ bvx*(ax0+ay0-bx0-by0) + bvx*(avx+avy)*t1

        bvx*(ax0+ay0)+bvx*(avx+avy)*t1 + bvy*(ax0+ay0)+bvy*(avx+avy)*t1 - bvx*(avx+avy)*t1 = bx0+by0+ bvx*(ax0+ay0-bx0-by0)
        """
        """WRONG manual
        t1denom = bvx * (avx + avy) + bvy * (avx + avy) - bvx * (avx + avy)
        assert t1denom
        t1 = (
            bx0
            + by0
            + bvx * (ax0 + ay0 - bx0 - by0)
            - bvx * (ax0 + ay0)
            - bvy * (ax0 + ay0)
        ) / t1denom
        t2 = (ax0 + ay0 + (avx + avy) * t1 - bx0 - by0) / (bvx + bvy)
        """
        # from sympy
        if (avx * bvy - avy * bvx) == 0:
            ####print("parallel", a, b)
            continue
        t1 = (-ax0 * bvy + ay0 * bvx - bvx * by0 + bvy * bx0) / (
            avx * bvy - avy * bvx
        )
        t2 = (avx * ay0 - avx * by0 - avy * ax0 + avy * bx0) / (
            avx * bvy - avy * bvx
        )
        """
        # xmin <= ax(t1) = bx(t2) <= xmax
        # ymin <= ay(t1) = by(t2) <= ymax
        # t1 >= 0, t2 >= 0
        # lines:
        # - parallel -> nothing in the input
        # ax0 + avx*t1 = bx0 + bvx*t2
        # ay0 + avy*t1 = by0 + bvy*t2
        """
        ax = ax0 + avx * t1
        ay = ay0 + avy * t1
        bx = bx0 + bvx * t2
        by = by0 + bvy * t2
        assert math.isclose(ax, bx)
        assert math.isclose(ay, by)
        # - intersect future within test area
        # - intersect in the past
        # - intersect outside test area
        assert t1
        assert t2
        intersected = (
            (t1 >= 0)
            and (t2 >= 0)
            and xmin <= ax <= xmax
            and ymin <= ay <= ymax
        )
        # if intersected:
        #     print(a, b, ax, ay)
        answer += intersected
    print(answer)
    return answer


def main():
    test_getanswer()

    date = dict(day=24, year=2023)
    aocd.submit(
        getanswer(aocd.get_data(**date), 200000000000000, 400000000000000),
        part="a",
        **date
    )


def test_getanswer():
    for data, min_, max_, expected_answer in [
        (
            """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""",
            7,
            27,
            2,
        ),
    ]:
        assert expected_answer == getanswer(data, min_, max_)
        print("\n\n")


if __name__ == "__main__":
    main()

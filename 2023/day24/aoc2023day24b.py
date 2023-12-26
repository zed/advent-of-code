#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/24#part1
- what is the key insight that enabled the solution?
  -> exclude t_i (convert parametric form to classic x,y)
- what is the longest bug to fix?
- what would have made it less likely?
"""
import sys
from typing import NamedTuple

from sympy import solve, symbols


class Heil(NamedTuple):
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


def getanswer(data):
    # parse input
    heil = [
        Heil(*map(int, line.replace("@", ",").split(",")))
        for line in data.splitlines()
    ]

    """

    Find x,v such that:
    - we know there _are_ such x, v
    - x :: integer
    - v :: integer
    - t_i :: integer?
      + t_i >= 0


    $x+v*t_i=x_{heil_i}+v_{heil_i}*t_i$
    - [ ] can t_i == t_j?

    n+2 unknowns
    3*n equations, non-linear
    """

    #  x_t=x+v*t_i=x_i+v_i*t_i
    #     =>
    #  a*x+b*v=c
    # Exclude t, convert to x, y, z form:
    # xt = x + vx*ti = xi+vxi*ti
    # yt = y + vy*ti = yi+vyi*ti
    # zt = z + vz*ti = zi+vzi*ti
    #
    """
    x + vx*ti = xi+vxi*ti ->
    ti*(vx-vxi) = xi-x    ->
    ti = (xi-x)/(vx-vxi)
    """
    x, y, z, vx, vy, vz = symbols("x,y,z, vx,vy,vz", integer=True)
    eqs = []
    for h in heil:
        # ti = (h.x-x)/(vx-h.vx)
        # yt = y + vy*ti = yi+vyi*ti
        eqs.append((y - h.y) * (vx - h.vx) + (vy - h.vy) * (h.x - x))
        # zt = z + vz*ti = zi+vzi*ti
        eqs.append((z - h.z) * (vx - h.vx) + (vz - h.vz) * (h.x - x))
    solutions = solve(eqs, [x, y, z, vx, vy, vz], dict=True)
    for sol in solutions:
        print(sol)
        for h in heil:
            # ti = (h.x-x)/(vx-h.vx)
            if vx == h.vx:
                print(
                    f"Reject solution due to vx == h.vx ({vx=}, {h.vx=})",
                    file=sys.stderr,
                )
                break
        else:  # no break: all vx!=h.vx
            # check t>=0
            # ti = (h.x-x)/(vx-h.vx)
            # sign(h.x-sol[x]) == sign(vx-h.vx)
            if all((h.x >= sol[x]) == (sol[vx] >= h.vx) for h in heil):
                # t >= 0
                answer = sum(map(sol.__getitem__, [x, y, z]))
                print(answer)
                return int(answer)
            else:
                print("ti is negative (ti = (h.x-x)/(vx-h.vx))")
    assert 0, "no solution"


def main():
    test_getanswer()


def test_getanswer():
    for data, expected_answer in [
        (
            """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""",
            (24 + 13 + 10),
        ),
        (open("input.txt").read().strip(), 571093786416929),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

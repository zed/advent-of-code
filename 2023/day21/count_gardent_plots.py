#!/usr/bin/env pypy
"""Usage: pypy count_garden_plots.py <nperiods> <grid-file>

Modified from memory:
https://www.youtube.com/watch?v=xHIQ2zHVSjM
"""
import sys

GPlot = complex


class Elf:
    def __init__(self, grid):
        self.grid_size = len(grid)
        # gardent plots reached at step 0 (the starting point)
        self.garden_plots = set(
            GPlot(r, c)
            for r, row in enumerate(grid)
            for c, ch in enumerate(row)
            if ch == "S"
        )
        self.rocks = frozenset(
            GPlot(r, c)
            for r, row in enumerate(grid)
            for c, ch in enumerate(row)
            if ch == "#"
        )

    def step(self):
        gp_next = set()
        for gp in self.garden_plots:
            # try moving in all four directions
            for d in [1, -1, 1j, -1j]:
                gpn = gp + d
                if self.wrap(gpn) not in self.rocks:
                    gp_next.add(gpn)
        self.garden_plots = gp_next

    def wrap(self, gp):
        return GPlot(gp.real % self.grid_size, gp.imag % self.grid_size)


def main():
    if len(sys.argv) != 3:
        exit(__doc__)
    nperiods = int(sys.argv[1])
    grid = tuple(open(sys.argv[2]).read().strip().splitlines())
    grid_size = len(grid)
    elf = Elf(grid)
    for nsteps in range(grid_size * nperiods + grid_size // 2 + 1):
        if (nsteps - grid_size // 2) % grid_size == 0:
            # print reached garden plots every period
            print(len(elf.garden_plots))
        elf.step()


if __name__ == "__main__":
    main()

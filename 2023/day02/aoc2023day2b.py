"""
https://adventofcode.com/2023/day/2#part2

fewest number of cubes of each color
"""
import re
import sys
from functools import reduce
from operator import mul


def fewest_number_of_cubes(game):
    m = re.fullmatch(r"Game\s+(\d+):\s+(.*)", game)
    assert m, f"{game=}"
    game_id = int(m[1])
    min_cubes = dict(red=0, green=0, blue=0)
    for subset in m[2].split(";"):
        for cube in subset.split(","):
            if not cube.strip():
                continue  # skip empty subsets
            n, color = cube.split()
            if int(n) > min_cubes[color]:
                min_cubes[color] = int(n)
    return min_cubes


def power(cubes):
    return reduce(mul, cubes.values())


print(
    sum(
        power(fewest_number_of_cubes(game))
        for game in map(str.rstrip, sys.stdin)
    )
)

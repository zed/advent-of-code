"""
https://adventofcode.com/2023/day/2#part1
"""
from typing import Optional

max_cubes = dict(red=12, green=13, blue=14)

import re
import sys


def possible_game(game: str) -> Optional[int]:
    """Return game id if it is possible, None otherwise."""
    m = re.fullmatch(r"Game\s+(\d+):\s+(.*)", game)
    if not m:
        assert 0, f"{game=}"
        return  # not a game
    game_id = int(m[1])
    for subset in m[2].split(";"):
        for cube in subset.split(","):
            if not cube.strip():
                continue  # skip empty subsets
            n, color = cube.split()
            if int(n) > max_cubes[color]:
                return  # impossible
    return game_id


def test_possible_game():
    assert possible_game("Game 12: ") == 12
    assert (
        possible_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
        == 1
    )


test_possible_game()
print(
    sum(
        gid
        for game in map(str.rstrip, sys.stdin)
        if (gid := possible_game(game))
    )
)

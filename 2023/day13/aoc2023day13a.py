#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/13#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)


def getanswer(data):
    patterns = list(filter(None, map(str.strip, data.split("\n\n"))))
    answer = sum(find_reflection(pattern.splitlines()) for pattern in patterns)
    print(answer)
    return answer


def find_reflection(grid):
    h = find_horizontal(grid)
    v = 0 if h else find_vertical(grid)
    return v + 100 * h


def find_horizontal(grid) -> int:
    """Find row of reflection if any.

    - 0 if none
    - i if line of reflection is between i and (i+1) rows
      (counting from 1)
    """
    return next(
        (h + 1 for h in range(len(grid)) if is_reflection_row(grid, h)), 0
    )


def find_vertical(grid) -> int:
    """Same as find_horizontal but for columns."""
    # ABC
    # abc
    # ->
    # aA
    # bB
    # cC
    return find_horizontal(rotate_clockwise(grid))


def rotate_clockwise(grid: list[str]) -> list[str]:
    return list(map("".join, zip(*grid[::-1])))


def main():
    test_answer()
    aocd.submit(getanswer(aocd.data))


def test_answer():
    assert rotate_clockwise(["ABC", "abc"]) == ["aA", "bB", "cC"]
    assert is_reflection_row(
        """\
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".splitlines(),
        3,
    )
    for i in set(range(7)) - {3}:
        assert not is_reflection_row(
            """\
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".splitlines(),
            i,
        )

    for data, expected_answer in [
        (
            """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""",
            405,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


def is_reflection_row(grid, h) -> bool:
    """Whether there is a reflection line between h & (h+1) rows."""
    return (h + 1) < len(grid) and all(
        up == down for up, down in zip(grid[: h + 1][::-1], grid[h + 1 :])
    )


if __name__ == "__main__":
    main()

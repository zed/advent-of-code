#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/14#part2
- what is the key insight that enabled the solution?
  -> there is a shorter cycle
- what is the longest bug to fix?
  -> original representation differs from transformed
  (it prevented detecting the cycle)
- what would have made it less likely?
  -> don't rush, validate each step
"""
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)

NCYCLES = 1000000000


def data2grid(data):
    return rotated(rotated(data.splitlines()))


def grid2data(grid):
    return "\n".join(grid)


def getanswer(data):
    grid = data2grid(data)
    seen = {grid: 0}
    for n in range(1, NCYCLES + 1):
        grid = cycled(grid)
        if grid in seen:
            break
        seen[grid] = n
    else:  # no break
        return getload(grid)
    # found shorter cycle
    # xy AbcAbcAb
    # 01 23456789
    # ...01201201
    #  3   = 5 - 2
    period = n - seen[grid]
    print(f"{period=}")
    # NCYCLES=9
    # 9-2 % 3 = 1
    # + 2 = 3 -> b
    j = ((NCYCLES - seen[grid]) % period) + seen[grid]
    G = next(G for G, i in seen.items() if i == j)
    answer = getload(G)
    print(answer)
    return answer


def cycled(grid):
    """N -> W -> S -> E"""
    # N
    """
    ABC
    123
    rotated
    A1
    B2
    C3
    moved_west
    """
    grid = rotated(grid)
    grid = moved_west(grid)
    # W
    # ABC
    # 123
    grid = rotated(grid)
    grid = moved_west(grid)
    # S
    # 1A
    # 2B
    # 3C
    grid = tuple(row[::-1] for row in rotated(grid))
    grid = moved_west(grid)
    # E
    # CBA
    # 321
    grid = tuple(row[::-1] for row in rotated(grid)[::-1])
    grid = moved_west(grid)

    grid = tuple(row[::-1] for row in grid)
    return grid


def moved_west(grid):
    return tuple(
        "#".join(
            [
                "O" * no_obstacles.count("O") + "." * no_obstacles.count(".")
                for no_obstacles in row.split("#")
            ]
        )
        for row in grid
    )


def p(grid):
    print("\n".join(map("".join, grid)), end="\n\n")


def rotated(grid):
    """
    ABC     A 1
    123 --> B 2
            C 3
    """
    return tuple(map("".join, zip(*grid)))


def getload(grid):
    """
    The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on
    """
    return sum(
        load * row.count("O") for load, row in enumerate(grid[::-1], start=1)
    )


def main():
    test_getanswer()
    ####aocd.submit(getanswer(aocd.data))


def test_cycled():
    for data, expected_answer in [
        (
            """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""",
            """\
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....""",
        ),
        (
            """\
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....""",
            """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O""",
        ),
        (
            """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O""",
            """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O""",
        ),
    ]:
        if (got := grid2data(cycled(data2grid(data)))) != expected_answer:
            print("<<<")
            print(got)
            print("--")
            print(expected_answer)
            print(">>>")
            assert got == expected_answer


def test_getload():
    for data, expected_answer in [
        (
            """\
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....""".splitlines(),
            136,
        ),
    ]:
        assert expected_answer == getload(data)
        print("\n\n")


def test_getanswer():
    for data, expected_answer in [
        (
            """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""",
            64,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

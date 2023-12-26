#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/14#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)


def getanswer(data):
    answer = getload(tilted(list(map(list, data.splitlines()))))
    print(answer)
    return answer


def tilted(grid):
    """Move round rocks up until edge or #."""
    grid = rotated(grid)
    for c, col in enumerate(grid):
        move(col)
    return rotated(grid)


def move(a):
    """Move rocks to the left."""
    end = 0
    while end < (len(a) - 1):
        # find free spot
        for end in range(end, len(a)):
            if a[end] == ".":
                break
        else:  # not found
            return

        # find rock
        for i in range(end, len(a)):
            if a[i] == "#":
                end = i + 1
                break
            elif a[i] == "O":
                break
        else:  # not found
            return

        if end > i:
            continue  # find free spot

        if end >= (len(a) - 1):
            return

        # move
        assert end < i
        assert a[i] == "O"
        assert a[end] == "."
        assert "#" not in a[end:i]
        a[end], a[i] = a[i], a[end]
        end += 1


def test_move():
    for data, expected_answer in [
        (list("###"), list("###")),
        (list("OOO"), list("OOO")),
        (list("..."), list("...")),
        (list(".O#"), list("O.#")),
        (list("..#"), list("..#")),
        (list("..O"), list("O..")),
        (list(".O."), list("O..")),
        (list(".#."), list(".#.")),
        (list(".#O"), list(".#O")),
        (list(".#.O"), list(".#O.")),
        (list("##.O"), list("##O.")),
        (list(".##.O"), list(".##O.")),
        (list("O.##.O"), list("O.##O.")),
        (list(".O##.O"), list("O.##O.")),
        (list(".O##..O"), list("O.##O..")),
    ]:
        orig = list(data)
        move(data)
        assert data == expected_answer, orig


def rotated(grid):
    return list(map(list, zip(*grid)))


def getload(grid):
    """
    The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on
    """
    return sum(
        load * row.count("O") for load, row in enumerate(grid[::-1], start=1)
    )


def main():
    test_getanswer()
    aocd.submit(getanswer(aocd.data))


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
            136,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

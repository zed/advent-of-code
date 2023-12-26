#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/12#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import re
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)


def getanswer(data):
    return sum(
        count_arrangements(row, tuple(map(int, broken.split(","))))
        for line in data.splitlines()
        if line.strip()
        for row, broken in [line.split()]
    )


def main():
    test_answer()
    aocd.submit(getanswer(aocd.data))


def count_arrangements(row, broken):
    # brute force
    return sum(count_broken(r) == broken for r in all_replacements(row))


def count_broken(row):
    assert "?" not in row
    return tuple(map(len, re.findall("#+", row)))


def all_replacements(row, start=0):
    if "?" not in row:
        yield row
    else:
        for i in range(start, len(row)):
            if row[i] == "?":
                yield from all_replacements(
                    row[:i] + "#" + row[i + 1 :], start=i + 1
                )
                yield from all_replacements(
                    row[:i] + "." + row[i + 1 :], start=i + 1
                )


def test_answer():
    for data, expected_answer in [
        ("#", ["#"]),
        (".", ["."]),
        ("?", ["#", "."]),
        ("?.", ["#.", ".."]),
        (
            "?.?",
            [
                "#.#",
                "#..",
                "..#",
                "...",
            ],
        ),
    ]:
        assert list(all_replacements(data)) == expected_answer
    for data, expected_answer in [
        ["#.#.###", (1, 1, 3)],
        [".#...#....###.", (1, 1, 3)],
        [".#.###.#.######", (1, 3, 1, 6)],
        ["####.#...#...", (4, 1, 1)],
        ["#....######..#####.", (1, 6, 5)],
        [".###.##....#", (3, 2, 1)],
    ]:
        assert count_broken(data) == expected_answer

    for data, expected_answer in [
        (
            """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""",
            (1, 4, 1, 1, 4, 10),
        ),
    ]:
        assert sum(expected_answer) == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

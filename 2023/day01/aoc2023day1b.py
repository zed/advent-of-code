"""
https://adventofcode.com/2023/day/1#part2
"""
import sys
from operator import attrgetter
from typing import NamedTuple


class Value(NamedTuple):
    index_first: int
    index_last: int
    digit: int


# note: ignore zeros i.e., "one0" -> 11
DIGITS = (
    "one two three four five six seven eight nine 1 2 3 4 5 6 7 8 9".split()
)


def digit2int(digit: str) -> int:
    v = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }.get(digit)
    if v is None:
        v = int(digit)
    return v


def calibration_value(line: str) -> int:
    assert line.casefold() == line
    assert line.encode("ascii").decode() == line
    assert "zero" not in line
    assert "0" not in line

    values = [
        Value(i, j, digit2int(digit))
        for digit in DIGITS
        if (i := line.find(digit)) >= 0 and (j := line.rfind(digit)) >= 0
    ]
    value = (
        min(values, key=attrgetter("index_first")).digit * 10
        + max(values, key=attrgetter("index_last")).digit
    )
    return value


print(sum(map(calibration_value, sys.stdin)))

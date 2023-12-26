#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/12#part2
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import functools
import re
import aocd
from rich import print

from rich.traceback import install

install(show_locals=True)


def getanswer(data):
    N = 5
    return sum(
        count_arrangements(
            "?".join([row] * N),
            tuple(map(int, ",".join([broken] * N).split(","))),
        )
        for line in data.splitlines()
        if line.strip()
        for row, broken in [line.split()]
    )


def main():
    test_answer()
    aocd.submit(getanswer(aocd.data))


@functools.cache
def count_arrangements(row, broken) -> int:
    # note: avoid O(2**count('?')) behavior

    row = row.strip(".")
    if not row:  # empty
        return not broken  # count as 1 if no broken expected
    if not broken:
        return "#" not in row  # count as 1 if no broken left

    first = row[0]
    ndamaged = broken[0]
    count = 0
    if first in "#?":  # broken branch
        # chop damaged group
        group = row[:ndamaged]
        if (
            len(group) == ndamaged  # enough length
            # next ndamaged shouldn't contain operational springs
            and "." not in group
            # must end or continue with operational spring
            and (len(row) == ndamaged or row[ndamaged] != "#")
        ):
            # +1 is to skip '.?' (that must separate broken groups)
            count += count_arrangements(row[ndamaged + 1 :], broken[1:])
    if first == "?":  # operational branch
        count += count_arrangements(row[1:], broken)
    return count


def test_answer():
    for data, expected_answer in [
        (
            """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""",
            (1, 16384, 1, 16, 2500, 506250),
        ),
    ]:
        assert sum(expected_answer) == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

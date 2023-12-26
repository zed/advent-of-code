#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/4#part2
"""
import aocd

lines = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".splitlines()
##lines = aocd.data.splitlines()


def s2n(s: str) -> set[str]:
    """Space-separated unique items to set of items (numbers)."""
    L = s.split()
    S = set(L)
    assert len(L) == len(S), s
    return S


def match_count(line):
    win, got = map(s2n, line.rpartition(":")[2].partition("|")[::2])
    return len(win & got)


matches = list(map(match_count, lines))
ncards = [1] * len(matches)
for i, (n, m) in enumerate(zip(ncards, matches)):
    for j in range(1, m + 1):
        ncards[i + j] += n

answer = sum(ncards)
print(answer)
##aocd.submit(answer)

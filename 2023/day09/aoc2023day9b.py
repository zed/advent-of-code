#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/9#part2
"""
import aocd


def diffs(seq):
    return [b - a for a, b in zip(seq, seq[1:])]


def prev_value(seq):
    first_values = []
    while True:
        first_values.append(seq[0])
        seq = diffs(seq)
        if all(n == 0 for n in seq):
            break
    prev = 0
    for first in first_values[::-1]:
        prev = first - prev
    return prev


def getanswer(data):
    histories = [list(map(int, line.split())) for line in data.splitlines()]
    return sum(map(prev_value, histories))


def main():
    data = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
    data = aocd.data
    print(data)
    answer = getanswer(data)
    print(answer)
    ##aocd.submit(answer)


if __name__ == "__main__":
    main()

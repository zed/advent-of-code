#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/9#part1
"""
import aocd


def diffs(seq):
    return [b - a for a, b in zip(seq, seq[1:])]


def next_value(seq):
    last_values = []
    while True:
        last_values.append(seq[-1])
        seq = diffs(seq)
        if all(n == 0 for n in seq):
            break
    next_ = 0
    for last in last_values[::-1]:
        next_ += last
    return next_


def getanswer(data):
    histories = [list(map(int, line.split())) for line in data.splitlines()]
    return sum(map(next_value, histories))


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
    ####aocd.submit(answer)


if __name__ == "__main__":
    main()

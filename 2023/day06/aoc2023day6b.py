#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/6#part2
"""
import aocd


def nways(T, D):
    # number of ways to win the race
    # (T-h)*h > D
    print(T, D)
    return sum((((T - h) * h) > D) for h in range(T))


def getanswer(data):
    # boat the farthest
    # go farther
    # hold time, release go
    # millis, mm
    T, D = [
        int("".join(line.partition(":")[2].split()))
        for line in data.splitlines()
        if line.strip()
    ]
    answer = nways(T, D)
    assert isinstance(answer, (int, str))
    return answer


def main():
    data = """\
Time:      7  15   30
Distance:  9  40  200
 """
    ###print(aocd.data)
    ###data = aocd.data
    answer = getanswer(data)
    print(answer)
    ###aocd.submit(answer)


if __name__ == "__main__":
    main()

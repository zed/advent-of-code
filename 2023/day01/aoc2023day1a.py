"""
https://adventofcode.com/2023/day/1
"""
import sys


def first_digit(line):
    # are there  multi code point digits?
    # is isdecimal vs. isdigit significant here
    for char in line:
        if char.isdecimal():
            return int(char)


def last_digit(line):
    return first_digit(reversed(line))


print(sum(first_digit(line) * 10 + last_digit(line) for line in sys.stdin))

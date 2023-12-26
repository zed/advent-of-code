#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/15#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""
import aocd
import pytest
from rich import print

from rich.traceback import install

install(show_locals=True)


def getanswer(data):
    strings = "".join(data.splitlines()).split(",")
    answer = sum(map(gethash, strings))
    print(answer)
    return answer


def main():
    test_getanswer()
    aocd.submit(getanswer(aocd.data))


def gethash(text: "ascii") -> range(0x100):
    h = 0
    for c in text.encode("ascii"):
        h += c
        h *= 17
        h %= 0x100
    return h


@pytest.mark.parametrize("text, expected", [("HASH", 52)])
def test_gethash(text, expected):
    assert gethash(text) == expected


def test_getanswer():
    for data, expected_answer in [
        (
            """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,
pc-,pc=6,ot=7
""",
            1320,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

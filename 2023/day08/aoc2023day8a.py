#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/8#part1
"""
import re
from collections import namedtuple
from itertools import cycle

import aocd
from rich import print

START_NODE, FINAL_NODE = "AAA", "ZZZ"
Node = namedtuple("Node", "name left right")


def getanswer(data):
    instructions, network_data = data.split("\n\n")
    L = "[A-Z]" * 3
    G = {
        m[0]: Node(*m)
        for line in network_data.splitlines()
        if (m := re.findall(L, line))
    }
    node = G[START_NODE]
    assert START_NODE != FINAL_NODE
    for nsteps, dir_ in enumerate(
        cycle("".join(instructions.split())), start=1
    ):
        if dir_ == "L":
            node = G[node.left]
        elif dir_ == "R":
            node = G[node.right]
        else:
            assert 0, f"{dir_=}"
        if node.name == FINAL_NODE:
            return nsteps
    assert 0, "didn't reach the final node"


def main():
    data = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
    data = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
    data = aocd.data
    answer = getanswer(data)
    print(answer)
    ##aocd.submit(answer)


if __name__ == "__main__":
    main()

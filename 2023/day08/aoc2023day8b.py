#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/8#part2

Key insight:
- there are exactly 6 (for each starting node) cycles
  (found by looking at force-atlas-gephi-6-cycles.png)
  -> lcm len(instructions), *cycles lengths
"""
import re
from collections import namedtuple
from itertools import cycle
from math import lcm

import aocd
from rich import print

Node = namedtuple("Node", "name left right")


def getanswer(data):
    instructions, network_data = data.split("\n\n")
    instructions = "".join(instructions.split())  # remove whitespace if any
    L = "[0-9A-Z]" * 3
    G = {
        m[0]: Node(*m)
        for line in network_data.splitlines()
        if (m := re.findall(L, line))
    }
    nodes = {node for node in G.values() if node.name.endswith("A")}
    # find lengths of 6 cycles
    def nsteps(node):
        for nsteps_, dir_ in enumerate(cycle(instructions), start=1):
            if dir_ == "L":
                node = G[node.left]
            elif dir_ == "R":
                node = G[node.right]
            else:
                assert 0, f"{dir_=}"
            if node.name.endswith("Z"):
                return nsteps_
        assert 0, "didn't reach the final node"

    lengths = list(map(nsteps, nodes))
    # find least common multiple of them
    assert lcm(*lengths) == lcm(len(instructions), *lengths)
    return lcm(*lengths)


def main():
    #
    """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
    #
    """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
    """
    #
    data = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
    data = aocd.data
    # print(data)
    answer = getanswer(data)
    print(answer)
    ###aocd.submit(answer)


if __name__ == "__main__":
    main()

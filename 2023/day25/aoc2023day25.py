#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/25#part1
- what is the key insight that enabled the solution?
  + gephi's openord visualization shows 3 edges connect two communities
    https://en.wikipedia.org/wiki/Community_structure
  + networkx.minimum_edge_cut() finds edges to remove
  + networkx.connected_components() returns connected components
- what is the longest bug to fix?
- what would have made it less likely?
- what utilities might have speed up similar solutions?
"""
import heapq
import math

import aocd
import datetime as DT
from collections import namedtuple

import networkx as nx
from icecream import ic

ic.configureOutput(prefix=lambda: f"{DT.datetime.now():%T}| ")


from rich.traceback import install

install(show_locals=True)

NCUTS = 3


def getanswer(data):
    ###data = open("input.txt").read().strip()
    # 3 wires -> 2 groups
    # union-find ? -> connected components
    G = nx.Graph()
    for line in data.splitlines():
        a, sep, rest = line.partition(":")
        assert sep
        for b in rest.split():
            G.add_edge(a, b)
    # nedges: 3473, math.comb(nedges, 3): 6975701096
    # too much for brute-force
    # look at the graph: openord
    ### nx.write_gexf(G, "aoc2023day25a.gexf")
    # find edges to cut, to get two connected components
    # there are exactly 3 such edges (in both puzzle & example inputs)
    # we need to find minimal cut

    ####DEAD for c in heapq.nlargest(2, nx.find_cliques(G), key=len): -> deadend
    ####assert nx.is_k_edge_connected(G, 3) -> works
    cutset = nx.minimum_edge_cut(G)
    for e in cutset:
        G.remove_edge(*e)
    size1, size2 = map(len, nx.connected_components(G))
    answer = size1 * size2
    print(answer)
    return answer


def main():
    test_getanswer()
    date = dict(day=25, year=2023)
    aocd.submit(getanswer(aocd.get_data(**date)), part="a", **date)


def test_getanswer():
    for data, expected_answer in [
        (
            """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""",
            54,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

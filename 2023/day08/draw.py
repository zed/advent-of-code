#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/8#part2
"""
import re
from collections import namedtuple
from itertools import cycle

import aocd
import networkx as nx
import matplotlib.pyplot as plt
from rich import print

Node = namedtuple("Node", "name left right")


def save_graph(graph, file_name):
    # from
    # https://stackoverflow.com/questions/17381006/large-graph-visualization-with-python-and-networkx
    # initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis("off")
    fig = plt.figure(1)
    pos = nx.circular_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name, bbox_inches="tight")


def save_gexf(graph, filename):
    nx.write_gexf(graph, filename)


def draw(data, filename):
    instructions, network_data = data.split("\n\n")
    L = "[0-9A-Z]" * 3
    G = nx.DiGraph()
    for line in network_data.splitlines():
        if m := re.findall(L, line):
            G.add_edge(m[0], m[1])
            G.add_edge(m[0], m[2])
    ##nx.draw(G, with_labels=True)
    ##plt.savefig(filename)
    ##save_graph(G, filename)
    save_gexf(G, filename)


def main():
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
    data = aocd.get_data(year=2023, day=8)
    print(data)
    draw(data, "aocd-day8b.gexf")


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/5#part1

Find the lowest location number that corresponds
to any of the initial seeds
"""
from collections import namedtuple
import aocd
from rich import print

# destination, source, length
# unmapped are one to one
almanac = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
####almanac = aocd.data
seeds_data, *maps_data = almanac.split("\n\n")
seeds = sorted(map(int, seeds_data.rpartition(":")[2].split()))

MapRange = namedtuple("MapRange", "src dest")


def parse_map(map_data) -> list[MapRange]:
    return sorted(
        (
            MapRange(range(src, src + n), range(dest, dest + n))
            for line in map_data.rpartition(":")[2].splitlines()
            if line.strip()
            for dest, src, n in [map(int, line.split())]
        ),
        key=lambda mr: (mr.src.start, mr.src.stop),
    )


maps = list(map(parse_map, maps_data))
result = []
for x in seeds:
    for d in maps:
        for src, dest in d:
            if x < src.start:  # unmapped x
                break  # x -> x
            elif src.start <= x < src.stop:  # in range
                x = dest.start + (x - src.start)
                break
            # try next map
    result.append(x)
# find min location for given seeds
answer = min(result)
print(answer)
####aocd.submit(answer)

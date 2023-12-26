#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/5#part2
"""
from collections import namedtuple
import aocd

MapRange = namedtuple("MapRange", "src shift")


def seed_ranges(seeds_data):
    it = map(int, seeds_data.rpartition(":")[2].split())
    while True:
        start = next(it, None)
        if start is None:
            break
        start = int(start)
        yield range(start, start + int(next(it)))


def parse_map(map_data) -> list[MapRange]:
    return sorted(
        (
            MapRange(range(src, src + n), dest - src)
            for line in map_data.rpartition(":")[2].splitlines()
            if line.strip()
            for dest, src, n in [map(int, line.split())]
        ),
        key=lambda mr: (mr.src.start, mr.src.stop),
    )


def location_ranges(seed_range, maps):
    src_ranges = [seed_range]
    for d in maps:
        src_ranges = [
            dest_range
            for r in src_ranges
            for dest_range in map_ranges(map_=d, src_range=r)
        ]
    return src_ranges


def map_ranges(map_, src_range):
    """Map *src_range* into destination ranges according to *map_*."""
    r = src_range
    for src, shift in map_:
        # left/intersect/right
        if (
            r.stop <= src.start
        ):  # ( ) < >: left of current map -> unmapped in the current map
            yield r
            return
        elif src.stop <= r.start:  # < > ( ): right of current map range
            continue  # try next range in the same map
        # intersect:
        if r.start <= src.start and r.stop <= src.stop:  # ( < ) >
            if r.start < src.start:  # left part is unmapped
                yield range(r.start, src.start)  # unmapped
                r = range(src.start, r.stop)
                assert r
            # map
            assert r.start == src.start
            assert len(r) <= len(src)
            yield range(src.start + shift, r.stop + shift)
            return
        elif r.start <= src.start and src.stop <= r.stop:  # ( < > )
            if r.start < src.start:  # left part is unmapped
                yield range(r.start, src.start)  # unmapped
                r = range(src.start, r.stop)
            # map
            yield range(src.start + shift, src.stop + shift)
            if src.stop < r.stop:  # right of current map range
                r = range(src.stop, r.stop)
                assert r
                continue  # try next range in the same map
            else:
                assert src.stop == r.stop
                return
        elif src.start <= r.start and src.stop <= r.stop:  # < ( > )
            if r.start < src.stop:
                # map
                yield range(r.start + shift, src.stop + shift)
                if src.stop < r.stop:
                    r = range(src.stop, r.stop)
                    assert r
                    continue  # try next range in the same map
                else:
                    assert src.stop == r.stop
                    return
        elif src.start <= r.start and r.stop <= src.stop:  # < ( ) >
            yield range(r.start + shift, r.stop + shift)
            return
        else:
            assert 0, (r, src)
    # unmapped
    yield r


def get_answer(almanac):
    seeds_data, *maps_data = almanac.split("\n\n")
    sranges = sorted(seed_ranges(seeds_data), key=lambda r: r.start)
    maps = list(map(parse_map, maps_data))

    # find min location for given seeds
    return min(lr.start for r in sranges for lr in location_ranges(r, maps))


def main():
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
    answer = get_answer(almanac)
    print(answer)
    ####aocd.submit(answer)


if __name__ == "__main__":
    main()

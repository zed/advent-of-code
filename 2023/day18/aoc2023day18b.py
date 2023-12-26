#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/18#part2
- what is the key insight that enabled the solution?
  -> Pick's theorem to take into account external half-border area
- what is the longest bug to fix?
  -> an attempt to find the half-border area despite
  seeing Pick's theorem
- what would have made it less likely?
  -> need to read more similar solutions
"""
import re


def getanswer(data):
    # extract instructions
    y, x = 0, 0
    boundary_count = 0
    polygon = [(x, y)]
    for line in data.splitlines():
        m = re.fullmatch(r"[RLUD]\s+\d+\s+\(#(\w{6})\)", line)
        h = m[1]
        n = int(h[:5], 16)
        boundary_count += n
        match h[5]:
            case "0":  # R
                x += n
            case "1":  # D
                y -= n
            case "2":  # L
                x -= n
            case "3":  # U
                y += n
            case _:
                assert 0
        polygon.append((x, y))
    # P[0] = P[N]
    assert polygon[0] == polygon[-1]  # loop
    # trapezoid formula
    # https://en.wikipedia.org/wiki/Shoelace_formula
    A2 = abs(
        sum(
            (y + yn) * (x - xn)
            for (x, y), (xn, yn) in zip(polygon, polygon[1:])
        )
    )
    assert A2 & 1 == 0  # even
    # number of internal points / internal area
    # pick's theorem
    # A = iA + b/2 -1
    internal_count = (A2 - boundary_count) // 2 + 1
    answer = internal_count + boundary_count
    print(answer)
    return answer


def main():
    test_getanswer()


def test_getanswer():
    for data, expected_answer in [
        (
            """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""",
            952408144115,
        ),
        (open("input.txt").read().strip(), 82712746433310),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

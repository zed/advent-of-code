#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/18#part1
- what is the key insight that enabled the solution?
- what is the longest bug to fix?
- what would have made it less likely?
"""


def getanswer(data):
    # trench #, ground .
    r, c = 0, 0
    trench = [(r, c)]
    boundary_count = 0  # number of boundary points?
    for line in data.splitlines():
        dir_, n, _ = line.split()
        n = int(n)
        boundary_count += n
        match dir_:
            case "R":
                c += n
            case "D":
                r += n
            case "L":
                c -= n
            case "U":
                r -= n
        trench.append((r, c))
    print(boundary_count)  # perimetr
    # interior
    # trapezoid formula
    # https://en.wikipedia.org/wiki/Shoelace_formula
    A2 = abs(
        sum(
            (y + yn) * (x - xn) for (x, y), (xn, yn) in zip(trench, trench[1:])
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
            62,
        ),
        (open("input.txt").read().strip(), 50465),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/15#part2
- what is the key insight that enabled the solution?
  -> no insights, just straightforward implementation from the spec
- what is the longest bug to fix?
- what would have made it less likely?
"""
import re
from collections import namedtuple
import aocd
import pytest
from rich import print

from rich.traceback import install

install(show_locals=True)

Lens = namedtuple("Lens", "label length")


def getanswer(data):
    # 0..255 incl
    boxes: list[list[Lens]] = [[] for _ in range(0x100)]  # use dict+position?
    for instruction in "".join(data.splitlines()).split(","):
        # instruction = label operation [focal length]
        label, op, fl = re.split("(=|-)", instruction)
        assert op == "=" or op == "-"
        box = boxes[gethash(label)]
        i = next((i for i, lens in enumerate(box) if lens.label == label), -1)
        if op == "-":
            assert not fl
            # 1. remove lens with given label if any from the box
            # 2. move remaining lens forward in the box without changing order (if no lens with given label, then nothing happens)
            if i != -1:  # found
                del box[i]
        elif op == "=":
            # label = "focal length"
            new_lens = Lens(label, int(fl))
            assert 1 <= new_lens.length <= 9
            # - lens go into box
            # - lens marked with label
            if i != -1:
                # replace old lens
                box[i] = new_lens
            else:
                # add lens to box
                # add behind, don't move other lens
                box.append(new_lens)

    answer = sum(
        box_no * slot_no * lens.length  # focus power
        for box_no, box in enumerate(boxes, start=1)
        for slot_no, lens in enumerate(box, start=1)
    )
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
            145,
        ),
    ]:
        assert expected_answer == getanswer(data)
        print("\n\n")


if __name__ == "__main__":
    main()

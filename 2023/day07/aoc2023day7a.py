#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/7#part1
"""
from collections import namedtuple, Counter
import aocd


class HandType:
    FIVE = -1
    FOUR = -2
    FULL = -3
    THREE = -4
    TWO_PAIR = -5
    ONE_PAIR = -6
    HIGH = -7


ALL_LABELS = "AKQJT98765432"
label2strength = dict(
    (L, -s) for L, s in zip(ALL_LABELS, range(len(ALL_LABELS)))
)
Hand = namedtuple("Hand", "cards bid")
Label = namedtuple("Label", "label count")


def hand_type(cards):
    top, *rest = [
        Label(L, count) for L, count in Counter(cards).most_common(2)
    ]
    if top.count == 5:
        return HandType.FIVE

    [second] = rest
    if top.count == 4:
        return HandType.FOUR
    elif top.count == 3 and second.count == 2:
        return HandType.FULL
    elif top.count == 3 and second.count < 2:
        return HandType.THREE
    elif top.count == 2 and second.count == 2:
        return HandType.TWO_PAIR
    elif top.count == 2 and second.count < 2:
        return HandType.ONE_PAIR
    elif top.count == 1:
        return HandType.HIGH
    assert 0, f"Can't happen {cards}"


def hand_key(hand):
    return (
        hand_type(hand.cards),
        tuple(map(label2strength.__getitem__, hand.cards)),
    )


def getanswer(hands_data):
    # bid \times rank
    hands = [
        Hand(cards, int(bid))
        for line in hands_data.splitlines()
        if line.strip()
        for cards, bid in [line.split()]
    ]
    return sum(
        rank * hand.bid
        for rank, hand in enumerate(sorted(hands, key=hand_key), start=1)
    )


def main():
    # hand bid
    hands_data = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
    ###hands_data = aocd.data
    answer = getanswer(hands_data)
    print(answer)
    ### aocd.submit(answer)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
https://adventofcode.com/2023/day/7#part2
"""
from enum import IntEnum
from collections import Counter
import aocd  # type: ignore


class HandType(IntEnum):
    FIVE = -1
    FOUR = -2
    FULL = -3
    THREE = -4
    TWO_PAIR = -5
    ONE_PAIR = -6
    HIGH = -7


ALL_LABELS = "AKQT98765432J"
J = "J"
label2strength = dict(
    (L, -s) for L, s in zip(ALL_LABELS, range(len(ALL_LABELS)))
)


def hand_type_no_joker(cards) -> HandType:
    top_count, *rest = [count for _, count in Counter(cards).most_common(2)]

    if top_count == 5:
        return HandType.FIVE

    [second_count] = rest
    return (
        HandType.FOUR
        if top_count == 4
        else HandType.FULL
        if top_count == 3 and second_count == 2
        else HandType.THREE
        if top_count == 3 and second_count < 2
        else HandType.TWO_PAIR
        if top_count == 2 and second_count == 2
        else HandType.ONE_PAIR
        if top_count == 2 and second_count < 2
        else HandType.HIGH  # if top_count == 1
    )


def hand_type(cards):
    return max(hand_type_no_joker(cards.replace(J, L)) for L in ALL_LABELS)


def hand_key(cards_bid):
    cards, *_ = cards_bid
    return (
        hand_type(cards),
        tuple(map(label2strength.__getitem__, cards)),
    )


def getanswer(hands_data):
    # bid \times rank
    hands = [
        (cards, int(bid))
        for line in hands_data.splitlines()
        if line.strip()
        for cards, bid in [line.split()]
    ]
    return sum(
        rank * bid
        for rank, (cards, bid) in enumerate(
            sorted(hands, key=hand_key), start=1
        )
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
    hands_data = aocd.data
    answer = getanswer(hands_data)
    print(answer)
    assert answer == 248909434
    ###aocd.submit(answer)


if __name__ == "__main__":
    main()

import time
from collections import Counter
from contextlib import contextmanager
from enum import IntEnum
from pathlib import Path
from typing import Callable, Literal

INPUT = "input.txt"


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        return fh.read().splitlines()


@contextmanager
def timer():
    start = time.perf_counter()
    yield
    stop = time.perf_counter()
    print("Duration:", stop - start)


Card = Literal["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


class HandType(IntEnum):
    HighCard = 1
    Pair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7


type Cards = tuple[Card, ...]
type Operator = Callable[[int, int], bool]


class Hand:
    card_values: dict[Card, int] = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    def __init__(self, card_string: str) -> None:
        self.cards: Cards = cards_from_string(card_string)
        self._type: HandType = get_hand_type_from_cards(self.cards)

    def __lt__(self, other: "Hand") -> bool:
        if self._type == other._type:
            for my_card, other_card in zip(self.cards, other.cards):
                if self.card_values[my_card] < self.card_values[other_card]:
                    return True
                elif self.card_values[my_card] > self.card_values[other_card]:
                    return False
        return self._type < other._type

    def __eq__(self, other: "Hand") -> bool:
        if self._type == other._type:
            for my_card, other_card in zip(self.cards, other.cards):
                if self.card_values[my_card] != self.card_values[other_card]:
                    return False
        return self._type == other._type

    def __gt__(self, other: "Hand") -> bool:
        if self._type == other._type:
            for my_card, other_card in zip(self.cards, other.cards):
                if self.card_values[my_card] > self.card_values[other_card]:
                    return True
                elif self.card_values[my_card] < self.card_values[other_card]:
                    return False
        return self._type > other._type


def cards_from_string(s) -> Cards:
    assert len(s) == 5
    return tuple(c for c in s)


class HandTypeNotFoundException(Exception):
    """Not a valid Hand!"""


def get_hand_type_from_cards(cards: Cards) -> HandType:
    counter = Counter(cards)
    values = counter.values()

    if all(c == 1 for c in values):
        return HandType.HighCard

    elif 2 in values:
        # Two Pair is the only case where we see two 2's in the counter's values.
        if 2 in Counter(values).values():
            return HandType.TwoPair
        # We can only see counts 2 AND 3 if we have a full house
        elif 3 in values:
            return HandType.FullHouse
        else:
            return HandType.Pair

    elif 3 in values:
        return HandType.ThreeOfAKind

    elif 4 in values:
        return HandType.FourOfAKind

    elif 5 in values:
        return HandType.FiveOfAKind

    raise HandTypeNotFoundException


def parse_line(line: str) -> tuple[Hand, int]:
    hand, bid = line.split()
    return Hand(hand), int(bid)


def solve_part_1(filename: str) -> int:
    lines = get_lines(filename)
    hands_and_bids: list[tuple[Hand, int]] = [parse_line(line) for line in lines]
    sorted_hands_and_bids = sorted(hands_and_bids, key=lambda h_b: h_b[0])
    total = 0
    for rank, h_b in enumerate(sorted_hands_and_bids, start=1):
        total += rank * h_b[1]
    return total


### Part 2


def get_hand_type_from_cards_with_jokers(cards: Cards) -> HandType:
    """
    If Jokers are allowed, we can build the strongest HandType by looking
    which card we already have most often (not counting the jokers themselves),
    and then making the joker(s) the same card.
    This works because there is no case where we want to create
    a TwoPair or FullHouse, because whenever we _could_ build those,
    we can also build ThreeOfAKind or FourOfAKind, respectively,
    which have a higher value.
    """
    non_joker_cards: Cards = tuple(card for card in cards if card != "J")
    joker_count = len(cards) - len(non_joker_cards)
    if joker_count == 5:
        best_cards: Cards = ("A",) * joker_count
    else:
        counter = Counter(non_joker_cards)
        most_common_card = counter.most_common(1)[0][0]
        best_cards: Cards = non_joker_cards + (most_common_card,) * joker_count

    if len(best_cards) != 5:
        raise ValueError("PANIC: Wrong number of Cards!")

    return get_hand_type_from_cards(best_cards)


class JokerHand(Hand):
    card_values: dict[Card, int] = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 1,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    def __init__(self, card_string: str) -> None:
        self.cards: Cards = cards_from_string(card_string)
        self._type: HandType = get_hand_type_from_cards_with_jokers(self.cards)


def parse_line_as_joker_hand(line: str) -> tuple[Hand, int]:
    hand, bid = line.split()
    return JokerHand(hand), int(bid)


def solve_part_2(filename: str) -> int:
    lines = get_lines(filename)
    hands_and_bids: list[tuple[Hand, int]] = [
        parse_line_as_joker_hand(line) for line in lines
    ]
    sorted_hands_and_bids = sorted(hands_and_bids, key=lambda h_b: h_b[0])
    total = 0
    for rank, h_b in enumerate(sorted_hands_and_bids, start=1):
        total += rank * h_b[1]
    return total


if __name__ == "__main__":
    with timer():
        print("Part 1:", solve_part_1(INPUT))
    with timer():
        print("Part 2:", solve_part_2(INPUT))

import puzzle
from puzzle import Cards, Hand, HandType, JokerHand

TEST_INPUT = "test_input.txt"


def test_get_high_card():
    given: Cards = puzzle.cards_from_string("AKQJT")
    want = HandType.HighCard
    got = puzzle.get_hand_type_from_cards(given)
    assert got == want


def test_get_pair():
    given: Cards = puzzle.cards_from_string("AAQJT")
    want = HandType.Pair
    got = puzzle.get_hand_type_from_cards(given)
    assert got == want


def test_get_two_pair():
    given: Cards = puzzle.cards_from_string("AAQQT")
    want = HandType.TwoPair
    got = puzzle.get_hand_type_from_cards(given)
    assert got == want


def test_get_three_of_a_kind():
    given: Cards = puzzle.cards_from_string("AAAQT")
    want = HandType.ThreeOfAKind
    got = puzzle.get_hand_type_from_cards(given)
    assert got == want


def test_get_full_hous():
    given: Cards = puzzle.cards_from_string("AAAQQ")
    want = HandType.FullHouse
    got = puzzle.get_hand_type_from_cards(given)
    assert got == want


def test_get_four_of_a_kind():
    given: Cards = puzzle.cards_from_string("AAAAT")
    want = HandType.FourOfAKind
    got = puzzle.get_hand_type_from_cards(given)
    assert got == want


def test_get_five_of_a_kind():
    given: Cards = puzzle.cards_from_string("AAAAA")
    want = HandType.FiveOfAKind
    got = puzzle.get_hand_type_from_cards(given)
    assert got == want


def test_compare_hands_with_different_types():
    hand_1: Hand = Hand("AAAAA")
    hand_2: Hand = Hand("23456")

    assert hand_1 > hand_2
    assert hand_2 < hand_1


def test_compare_hands_with_same_type():
    hand_1: Hand = Hand("AAT85")
    hand_2: Hand = Hand("AA234")

    assert hand_1 > hand_2
    assert hand_2 < hand_1


def test_compare_identical_hands():
    hand_1: Hand = Hand("AAT85")
    hand_2: Hand = Hand("AAT85")

    assert not hand_1 > hand_2
    assert not hand_2 < hand_1


def test_parse_line():
    given = "32T3K 765"
    want = Hand("32T3K"), 765
    got = puzzle.parse_line(given)
    assert got == want


def test_part_1():
    want = 6440
    got = puzzle.solve_part_1(TEST_INPUT)
    assert got == want

    want = 248105065
    got = puzzle.solve_part_1(puzzle.INPUT)
    assert got == want


def test_hand_without_jokers_stays_same():
    assert JokerHand("AAAAA")._type == HandType.FiveOfAKind
    assert JokerHand("AAAAK")._type == HandType.FourOfAKind
    assert JokerHand("AAAKK")._type == HandType.FullHouse
    assert JokerHand("AAAKQ")._type == HandType.ThreeOfAKind
    assert JokerHand("AAKKQ")._type == HandType.TwoPair
    assert JokerHand("AAKQT")._type == HandType.Pair
    assert JokerHand("AKQT9")._type == HandType.HighCard


def test_joker_makes_highcard_into_a_pair():
    got = JokerHand("AKQJT")._type
    want = HandType.Pair
    assert got == want


def test_joker_makes_pair_into_three_of_a_kind():
    got = JokerHand("AAKQJ")._type
    want = HandType.ThreeOfAKind
    assert got == want


def test_joker_makes_two_pair_into_full_house_a_par():
    got = JokerHand("AAKKJ")._type
    want = HandType.FullHouse
    assert got == want


def test_joker_makes_three_of_a_kind_into_four_of_a_kind():
    got = JokerHand("AAAKJ")._type
    want = HandType.FourOfAKind
    assert got == want


def test_joker_makes_four_of_a_kind_into_five_of_a_kind():
    got = JokerHand("AAAAJ")._type
    want = HandType.FiveOfAKind
    assert got == want


def test_two_jokers_make_full_house_into_five_of_a_kind():
    got = JokerHand("AAAJJ")._type
    want = HandType.FiveOfAKind
    assert got == want

    got = JokerHand("AAJJJ")._type
    want = HandType.FiveOfAKind
    assert got == want


def test_five_jokers_are_five_of_a_kind():
    got = JokerHand("JJJJJ")._type
    want = HandType.FiveOfAKind
    assert got == want


def test_part_2():
    want = 5905
    got = puzzle.solve_part_2(TEST_INPUT)
    assert got == want

    # want = 248105065
    # got = puzzle.solve_part_1(puzzle.INPUT)
    # assert got == want

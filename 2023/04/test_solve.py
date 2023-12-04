import solve

TEST_INPUT = "test_input.txt"


def test_winning_numbers_are_found():
    given = "Card 1: 2 3 99 | 4 5 6"
    want = set((2, 3, 99))
    got, _ = solve.parse_line(given)
    assert got == want


def test_my_numbers_are_found():
    given = "Card 1: 2 3 99 | 4 5 6"
    want = set((4, 5, 6))
    _, got = solve.parse_line(given)
    assert got == want


def test_get_number_of_matches():
    set_1: set[int] = set((2, 3))
    set_2: set[int] = set((2, 4))
    want = 1
    got = solve.get_number_of_matches(set_1, set_2)
    assert got == want


def test_calculate_points():
    given = [0, 1, 2, 3, 4]
    want = [0, 1, 2, 4, 8]
    for g, w in zip(given, want):
        got = solve.calculate_points(g)
        assert got == w


def test_part_1():
    want = 13
    got = solve.part_1(TEST_INPUT)
    assert got == want


def test_part_2():
    want = 30
    got = solve.part_2(TEST_INPUT)
    assert got == want

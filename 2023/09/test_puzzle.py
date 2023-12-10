import puzzle

TEST_INPUT = "test_input.txt"


def test_next_value_for_sequence():
    given = [10, 13, 16, 21, 30, 45]
    want = 68
    got = puzzle.calculate_next_value_for_sequence(given)
    assert got == want


def test_part_1_returns_correct_number():
    want = 2
    got = puzzle.solve_part_2(TEST_INPUT)
    assert got == want

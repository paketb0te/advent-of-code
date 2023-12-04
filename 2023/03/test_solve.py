import solve

TEST_INPUT = "test_input.txt"


def test_get_partnum_from_single_line():
    given = "...456..."
    want = [solve.PartNumber(start=3, end=5, line_no=0, number=456)]
    got = solve.parse_single_line(line=given, line_no=0)
    assert got == want


def test_get_two_partnums_from_single_line():
    given = "123...789"
    want = [
        solve.PartNumber(start=0, end=2, line_no=0, number=123),
        solve.PartNumber(start=6, end=8, line_no=0, number=789),
    ]
    got = solve.parse_single_line(line=given, line_no=0)
    assert got == want


def test_get_single_digit_partnum_from_start_of_line():
    given = "1."
    want = [solve.PartNumber(start=0, end=0, line_no=0, number=1)]
    got = solve.parse_single_line(line=given, line_no=0)
    assert got == want


def test_get_single_digit_partnum_from_end_of_line():
    given = ".9"
    want = [solve.PartNumber(start=1, end=1, line_no=0, number=9)]
    got = solve.parse_single_line(line=given, line_no=0)
    assert got == want


def test_get_partnums_split_for_new_lines():
    given = [
        "......789",
        "123......",
    ]
    want = [
        solve.PartNumber(start=6, end=8, line_no=0, number=789),
        solve.PartNumber(start=0, end=2, line_no=1, number=123),
    ]
    got = solve.parse_lines(lines=given)

    assert got == want


def test_get_partnum_from_multiple_lines():
    given = [
        "123......",
        "...456...",
        "......789",
    ]
    want = [
        solve.PartNumber(start=0, end=2, line_no=0, number=123),
        solve.PartNumber(start=3, end=5, line_no=1, number=456),
        solve.PartNumber(start=6, end=8, line_no=2, number=789),
    ]
    got = solve.parse_lines(lines=given)

    assert got == want


def test_get_adjacenct_field_coordinates():
    given = solve.PartNumber(start=3, end=5, line_no=1, number=456)
    previous_line_adj_coordinates = set(
        solve.Coordinates(x=x, y=0) for x in range(2, 7)
    )
    same_line_adj_coordinates = set(solve.Coordinates(x=x, y=1) for x in (2, 6))
    next_line_adj_coordinates = set(solve.Coordinates(x=x, y=2) for x in range(2, 7))

    want = (
        previous_line_adj_coordinates
        | same_line_adj_coordinates
        | next_line_adj_coordinates
    )
    got = given.get_adj_coordinates()

    assert got == want


def test_field_is_symbol():
    given = "&/*%=$+"

    for char in given:
        assert solve.is_symbol(char)


def test_dot_and_digits_are_not_symbols():
    given = ".1234567890"
    for char in given:
        assert not solve.is_symbol(char)


def test_part_1_returns_correct_sum():
    want = 4361
    got = solve.part_1(TEST_INPUT)
    assert got == want


def test_part_2():
    want = 467835
    got = solve.part_2(TEST_INPUT)
    assert got == want

import solve


def test_first_digit_is_recognized():
    given = "12three"
    want = 13
    got = solve.get_number_from_line_2(given)
    assert got == want


def test_last_digit_is_recognized():
    given = "one23"
    want = 13
    got = solve.get_number_from_line_2(given)
    assert got == want


def test_get_number_from_line_with_single_digits():
    given = "123"
    want = 13
    got = solve.get_number_from_line_2(given)
    assert got == want


def test_get_number_from_line_with_spelled_out_digits():
    given = "onetwothree"
    want = 13
    got = solve.get_number_from_line_2(given)
    assert got == want


def test_two_spelled_out_digits_with_one_single_digit_between():
    given = "one2three"
    want = 13
    got = solve.get_number_from_line_2(given)
    assert got == want


def test_two_single_digits_with_one_spelled_out_digit_between():
    given = "1two3"
    want = 13
    got = solve.get_number_from_line_2(given)
    assert got == want


def test_():
    given = "eightwothree"
    want = 83
    got = solve.get_number_from_line_2(given)
    assert got == want

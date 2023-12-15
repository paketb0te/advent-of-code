import puzzle


def test_hash():
    given = "HASH"
    want = 52
    got = puzzle.hash(given)
    assert got == want


def test_solve_part_1():
    want = 1320
    got = puzzle.solve_part_1(TEST_INPUT)
    assert got == want


def test_regex_parsing_with_assignment():
    given = "rn=1"
    want = puzzle.Step("rn", "=", 1)
    got = puzzle.parse_step(given)
    assert got == want


def test_regex_parsing_with_removal():
    given = "rn-"
    want = puzzle.Step("rn", "-", None)
    got = puzzle.parse_step(given)
    assert got == want


def test_solve_part_2():
    want = 145
    got = puzzle.solve_part_2(TEST_INPUT)
    assert got == want


TEST_INPUT = "test_input.txt"

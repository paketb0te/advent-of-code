import puzzle
from puzzle import Galaxy

TEST_INPUT = "test_input.txt"


def test_parse_galaxies():
    given = [
        "...#......",
        ".......#..",
    ]
    want = [Galaxy(0, 3), Galaxy(1, 7)]
    got = puzzle.parse_lines(given)
    assert got == want


def test_find_empty_lines():
    given = puzzle.get_lines(TEST_INPUT)
    want = [3, 7]
    got = puzzle.find_empty_line_indices(given)
    assert got == want


def test_find_empty_columns():
    given = puzzle.get_lines(TEST_INPUT)
    want = [2, 5, 8]
    got = puzzle.find_empty_column_indices(given)
    assert got == want


def test_calculate_simple_distance():
    given = (Galaxy(0, 0), Galaxy(1, -1))
    # We want the Manhattan distance between galaxies
    want = 2
    got = puzzle.calculate_distance(
        *given, empty_lines=[], empty_columns=[], space_factor=2
    )
    assert got == want


def test_calculate_distance_with_empty_lines():
    given = (Galaxy(0, 0), Galaxy(2, 0))
    empty_lines = [1]
    # the empty lines count double distance
    want = 3
    got = puzzle.calculate_distance(
        *given, empty_lines=empty_lines, empty_columns=[], space_factor=2
    )
    assert got == want


def test_calculate_distance_with_empty_columns():
    given = (Galaxy(0, 0), Galaxy(0, 2))
    empty_columns = [1]
    # the empty columns count double distance
    want = 3
    got = puzzle.calculate_distance(
        *given, empty_lines=[], empty_columns=empty_columns, space_factor=2
    )
    assert got == want


def test_calculate_distance_with_empty_lines_and_columns():
    given = (Galaxy(0, 0), Galaxy(2, 2))
    empty_lines = [1]
    empty_columns = [1]
    # the empty lines and columns count double distance
    want = 6
    got = puzzle.calculate_distance(
        *given, empty_lines=empty_lines, empty_columns=empty_columns, space_factor=2
    )
    assert got == want


def test_solve_part_1():
    want = 374
    got = puzzle.solve(TEST_INPUT, 2)
    assert got == want


def test_solve_part_2():
    want = 1030
    got = puzzle.solve(TEST_INPUT, 10)
    assert got == want

import puzzle

TEST_INPUT = "test_input.txt"


def test_find_number_of_columns_to_the_left_of_mirror_line():
    given = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]
    want = 5
    got = puzzle.find_number_of_columns(given)
    assert got == want


def test_find_number_of_rows_above_mirror_line():
    given = [
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]
    want = 4
    got = puzzle.find_number_of_rows(given)
    assert got == want

import pytest
import solve

TEST_INPUT = "test_input.txt"


def test_parse_lines():
    given = solve.get_lines(TEST_INPUT)
    # data from test_input.txt
    want = [
        solve.Race(time=7, dist=9),
        solve.Race(time=15, dist=40),
        solve.Race(time=30, dist=200),
    ]
    got = solve.parse_lines(given)
    assert got == want


def test_get_possible_distances_for_time():
    given = 2
    want = [0, 1, 0]
    got = list(solve.get_possible_distances_for_time(time=given))
    assert got == want

    given = 3
    want = [0, 2, 2, 0]
    got = list(solve.get_possible_distances_for_time(time=given))
    assert got == want

    given = 4
    want = [0, 3, 4, 3, 0]
    got = list(solve.get_possible_distances_for_time(time=given))
    assert got == want


def test_get_count_of_winning_possibilities_for_race():
    given = solve.Race(time=7, dist=9)
    want = 4
    got = solve.get_count_of_winning_possibilities_for_race(given)
    assert got == want

    given = solve.Race(time=15, dist=40)
    want = 8
    got = solve.get_count_of_winning_possibilities_for_race(given)
    assert got == want

    given = solve.Race(time=30, dist=200)
    want = 9
    got = solve.get_count_of_winning_possibilities_for_race(given)
    assert got == want


def test_part_1():
    want = 288
    got = solve.part_1(TEST_INPUT)
    assert got == want


def test_parse_lines_for_part_2():
    given = solve.get_lines(TEST_INPUT)
    # data from test_input.txt
    want = solve.Race(time=71530, dist=940200)
    got = solve.parse_lines_for_part_2(given)
    assert got == want


def test_part_2():
    ...
    want = 71503
    got = solve.part_2(TEST_INPUT)
    assert got == want

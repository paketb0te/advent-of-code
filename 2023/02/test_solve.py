import solve


def test_game_id_is_found():
    given = "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    want = 5
    got = solve.parse_line(given).id_
    assert got == want


def test_list_of_draws_is_found():
    given = "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    want = [{"red": 6, "green": 3, "blue": 1}, {"blue": 2, "red": 1, "green": 2}]
    got = solve.parse_line(given).draws
    assert got == want


def test_game_is_possible():
    given_cubes = {"red": 1, "green": 1, "blue": 1}
    given_draws = [{"red": 2, "green": 1, "blue": 1}, {"blue": 2, "red": 1, "green": 2}]
    want = False
    got = solve.draws_are_possible(given_draws, given_cubes)
    assert got == want

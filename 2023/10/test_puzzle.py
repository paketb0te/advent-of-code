import puzzle
import pytest
from puzzle import Position

TEST_INPUT = "test_input.txt"

# ".": (), () is ground; there is no pipe in this tile.
# "S": (), () is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


@pytest.fixture
def lines() -> list[str]:
    return [
        ".....",
        ".S-7.",
        ".|.|.",
        ".L-J.",
        ".....",
    ]


def test_get_next_position():
    previous_tile = puzzle.Tile(symbol="F", pos=Position(0, 0))
    current_tile = puzzle.Tile(symbol="|", pos=Position(1, 0))
    want = Position(2, 0)
    got = puzzle.get_next_position(
        current_tile=current_tile,
        previous_tile=previous_tile,
    )
    assert got == want


def test_find_S(lines: list[str]):
    want = puzzle.Tile(symbol="S", pos=Position(1, 1))
    got = puzzle.find_S(lines=lines)
    assert got == want


def test_get_surrounding_positions():
    given = Position(1, 1)
    want = [
        Position(0, 0),
        Position(0, 1),
        Position(0, 2),
        Position(1, 0),
        Position(1, 2),
        Position(2, 0),
        Position(2, 1),
        Position(2, 2),
    ]
    got = puzzle.get_surrounding_positions(given)
    assert got == want


def test_get_possible_steps_around_S(lines: list[str]):
    # These are the possible starting postions, given the test input
    want = (Position(1, 2), Position(2, 1))
    got = puzzle.get_starting_tile(lines=lines)
    assert got.pos in want


def test_solve_part_1():
    want = 8
    got = puzzle.solve_part_1(TEST_INPUT)
    assert got == want

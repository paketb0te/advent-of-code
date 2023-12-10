from typing import Generator
import puzzle

TEST_INPUT = "test_input.txt"


def test_parsing_line_as_map():
    given = "BBB = (AAA, ZZZ)"
    want = "BBB", {"L": "AAA", "R": "ZZZ"}
    got = puzzle.parse_line_as_map(given)
    assert got == want


def test_get_instruction_generator():
    given = "LLR"
    # Check the first few elements from the infinitely long list of instructions
    want = "LLRLLRL"

    instructions = puzzle.get_instructions(given)
    got = ""
    for _ in range(7):
        got += next(instructions)

    assert got == want


def test_build_map_of_maps_from_test_input():
    lines = puzzle.get_lines(filename=TEST_INPUT)
    want = {
        "AAA": {"L": "BBB", "R": "BBB"},
        "BBB": {"L": "AAA", "R": "ZZZ"},
        "ZZZ": {"L": "ZZZ", "R": "ZZZ"},
    }
    got = puzzle.build_map(lines)
    assert got == want


def test_solve_part_1():
    want = 6
    got = puzzle.solve_part_1(TEST_INPUT)
    assert got == want


def test_get_steps_for_finding_first_node_ending_in_Z():
    instructions = puzzle.get_instructions("LR")
    map_ = {
        "11A": {"L": "11B", "R": "XXX"},
        "11B": {"L": "XXX", "R": "11Z"},
        "11Z": {"L": "11B", "R": "XXX"},
    }

    start = "11A"

    want = 2
    got = puzzle.get_number_of_steps_to_reach_destination(
        start_node=start,
        found_check=lambda x: x.endswith("Z"),
        instructions=instructions,
        map_=map_,
    )

    assert got == want


def test_solve_part_2():
    want = 6
    got = puzzle.solve_part_2(TEST_INPUT)
    assert got == want

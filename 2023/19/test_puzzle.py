import puzzle

TEST_INPUT = "test_input.txt"


def test_parse_part_line():
    given = "{x=787,m=2655,a=1222,s=2876}"
    want = puzzle.Part(x=787, m=2655, a=1222, s=2876)
    got = puzzle.parse_part_line(given)
    assert got == want


def test_parse_workflow_line():
    given = "in{s<1351:px,qqz}"
    puzzle.Workflow(given)

    assert "in" in puzzle.WORKFLOW_MAP


def test_solve_part_1():
    assert puzzle.solve_part_1(TEST_INPUT) == 19114

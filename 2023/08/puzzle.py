import itertools
import math
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterable

INPUT = "input.txt"


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        return fh.read().splitlines()


@contextmanager
def timer():
    start = time.perf_counter()
    yield
    stop = time.perf_counter()
    print("Duration:", stop - start)


def parse_line_as_map(line: str) -> tuple[str, dict[str, str]]:
    key, nodes = line.split("=")
    left, right = nodes.split(",")

    key = key.strip()
    left = left.replace("(", "").strip()
    right = right.replace(")", "").strip()

    return key, {"L": left, "R": right}


def build_map(lines: list[str]) -> dict[str, dict[str, str]]:
    map_: dict[str, dict[str, str]] = {}
    for line in lines[2:]:
        k, v = parse_line_as_map(line)
        map_[k] = v

    return map_


def get_instructions(line: str):
    return itertools.cycle(line)


def solve_part_1(filename: str) -> int:
    lines = get_lines(filename)
    instructions = get_instructions(line=lines[0])
    map_ = build_map(lines)
    start_node = "AAA"
    found_check = lambda x: x == "ZZZ"

    return get_number_of_steps_to_reach_destination(
        start_node, found_check, instructions, map_
    )


def get_number_of_steps_to_reach_destination(
    start_node: str,
    found_check: Callable[[str], bool],
    instructions: itertools.cycle,
    map_: dict[str, dict[str, str]],
):
    current_node = start_node
    for step, instruction in enumerate(instructions, start=1):
        current_node = map_[current_node][instruction]
        if found_check(current_node):
            return step

    raise ValueError("Something _definitely_ went wrong...")


### Part 2


def solve_part_2(filename: str) -> int:
    lines = get_lines(filename)
    instructions = get_instructions(line=lines[0])
    map_ = build_map(lines)

    def found(node: str) -> bool:
        return node.endswith("Z")

    starting_nodes: Iterable[str] = (n for n in map_.keys() if n.endswith("A"))

    first_matches: Iterable[int] = (
        get_number_of_steps_to_reach_destination(
            start_node=node, found_check=found, instructions=instructions, map_=map_
        )
        for node in starting_nodes
    )
    return math.lcm(*first_matches)


if __name__ == "__main__":
    with timer():
        print("Part 1:", solve_part_1(INPUT))
    with timer():
        print("Part 2:", solve_part_2(INPUT))

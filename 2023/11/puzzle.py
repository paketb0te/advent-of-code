import itertools
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

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


@dataclass(frozen=True)
class Galaxy:
    i: int
    j: int


def parse_lines(lines: list[str]) -> Iterable[Galaxy]:
    galaxies = [
        Galaxy(i=i, j=j)
        for i, line in enumerate(lines)
        for j, char in enumerate(line)
        if char == "#"
    ]
    return galaxies


def find_empty_line_indices(lines: list[str]) -> list[int]:
    empty_indices: list[int] = []
    for i, line in enumerate(lines):
        if all(char != "#" for char in line):
            empty_indices.append(i)

    return empty_indices


def find_empty_column_indices(lines: list[str]) -> list[int]:
    empty_indices: list[int] = []
    for j in range(len(lines[0])):
        if all(lines[i][j] != "#" for i in range(len(lines))):
            empty_indices.append(j)

    return empty_indices


def calculate_distance(
    galaxy_1: Galaxy,
    galaxy_2: Galaxy,
    empty_lines: list[int],
    empty_columns: list[int],
    space_factor: int,
) -> int:
    expansions: int = 0

    for i in empty_lines:
        if (galaxy_1.i < i < galaxy_2.i) or (galaxy_1.i > i > galaxy_2.i):
            expansions += 1

    for j in empty_columns:
        if (galaxy_1.j < j < galaxy_2.j) or (galaxy_1.j > j > galaxy_2.j):
            expansions += 1

    return (
        abs(galaxy_1.i - galaxy_2.i)
        + abs(galaxy_1.j - galaxy_2.j)
        + expansions * (space_factor - 1)
    )


def solve(filename: str, space_factor: int) -> int:
    lines = get_lines(filename)
    galaxies = parse_lines(lines)
    empty_lines = find_empty_line_indices(lines)
    empty_columns = find_empty_column_indices(lines)
    pairs = list(itertools.combinations(galaxies, 2))

    return sum(
        calculate_distance(
            *pair,
            empty_lines=empty_lines,
            empty_columns=empty_columns,
            space_factor=space_factor,
        )
        for pair in pairs
    )


if __name__ == "__main__":
    with timer():
        print("Part 1:", solve(INPUT, space_factor=2))
    with timer():
        print("Part 2:", solve(INPUT, space_factor=1_000_000))

import time
from contextlib import contextmanager
from pathlib import Path

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


def calculate_next_value_for_sequence(sequence: list[int]) -> int:
    sub_sequences: list[list[int]] = [sequence]

    current_sequence = sequence
    while any(current_sequence):
        new_sequence = [
            current_sequence[i + 1] - current_sequence[i]
            for i in range(len(current_sequence) - 1)
        ]
        sub_sequences.append(new_sequence)
        current_sequence = new_sequence

    return sum(s[-1] for s in sub_sequences)


def solve_part_1(filename: str) -> int:
    sequences = [[int(n) for n in line.split()] for line in get_lines(filename)]
    return sum(calculate_next_value_for_sequence(s) for s in sequences)


## Part 2


def solve_part_2(filename: str) -> int:
    sequences = [[int(n) for n in line.split()] for line in get_lines(filename)]
    return sum(calculate_next_value_for_sequence(s[::-1]) for s in sequences)


if __name__ == "__main__":
    with timer():
        print("Part 1:", solve_part_1(INPUT))
    with timer():
        print("Part 2:", solve_part_2(INPUT))

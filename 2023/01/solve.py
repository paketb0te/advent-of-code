from pathlib import Path
from typing import Iterable

FILENAME = "input.txt"


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        lines = fh.readlines()
    return lines


def get_number_from_line(line: str) -> int:
    digits = [c for c in line if c.isdigit()]
    number = 10 * int(digits[0]) + int(digits[-1])
    return number


def part_1() -> None:
    lines = get_lines(FILENAME)
    total = sum(get_number_from_line(line) for line in lines)
    print("Part 1:", total)


MAPPING = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_ordered_substrings(line: str) -> list[str]:
    substrings: list[str] = []
    for start in range(len(line)):
        for end in range(start + 1, len(line) + 1):
            substring = line[start:end]
            substrings.append(substring)
    return substrings


def is_single_digit(__str: str) -> bool:
    return len(__str) == 1 and __str.isdigit()


def get_number_from_line_part_2(line: str) -> int:
    substrings = get_ordered_substrings(line)
    first = get_first_digit(substrings)
    last = get_first_digit(reversed(substrings))
    number = 10 * first + last
    return number


def get_first_digit(substrings: Iterable[str]) -> int:
    for substring in substrings:
        if is_single_digit(substring):
            return int(substring)

        number = MAPPING.get(substring)
        if number is not None:
            return number

    raise ValueError(f"no digit found in substrings: {substrings}")


def part_2() -> None:
    lines = get_lines(FILENAME)
    total = sum(get_number_from_line_part_2(line) for line in lines)
    print("Part 2:", total)


if __name__ == "__main__":
    part_1()
    part_2()

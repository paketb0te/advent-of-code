from pathlib import Path

INPUT = "input.txt"


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        return fh.read().splitlines()


def parse_line(line: str) -> tuple[set[int], set[int]]:
    _, numbers = line.split(":")
    winning_numbers_str, my_numbers_str = numbers.split("|")

    winning_numbers: set[int] = get_numbers_from_string(winning_numbers_str)
    my_numbers: set[int] = get_numbers_from_string(my_numbers_str)

    return winning_numbers, my_numbers


def get_numbers_from_string(string: str) -> set[int]:
    return set(int(n) for n in string.split())


def get_number_of_matches(set1: set[int], set2: set[int]) -> int:
    return len(set1 & set2)


def part_1(filename: str) -> int:
    lines = get_lines(filename)
    total = 0
    for line in lines:
        winning, my = parse_line(line=line)
        matches = get_number_of_matches(winning, my)
        points = calculate_points(matches)
        total += points

    return total


def calculate_points(matches: int) -> int:
    if matches == 0:
        return 0
    return 2 ** (matches - 1)


### Part 2


def part_2(filename: str) -> int:
    lines = get_lines(filename)
    card_copies = [1] * len(lines)
    for idx, line in enumerate(lines):
        winning, my = parse_line(line=line)
        matches = get_number_of_matches(winning, my)

        for following_idx in range(idx + 1, idx + 1 + matches):
            card_copies[following_idx] += card_copies[idx]

    return sum(card_copies)


if __name__ == "__main__":
    print("Part 1:", part_1(INPUT))
    print("Part 2:", part_2(INPUT))

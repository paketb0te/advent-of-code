from dataclasses import dataclass
from pathlib import Path

INPUT = "input.txt"


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        return fh.read().splitlines()


@dataclass
class Coordinates:
    x: int
    y: int


@dataclass
class PartNumber:
    start: int
    end: int
    line_no: int
    number: int

    def get_adj_coordinates(self) -> list[Coordinates]:
        previous_line_adj_coordinates: list[Coordinates] = [
            Coordinates(x=x, y=self.line_no - 1)
            for x in range(self.start - 1, self.end + 2)
        ]
        same_line_adj_coordinates = [
            Coordinates(x=self.start - 1, y=self.line_no),
            Coordinates(x=self.end + 1, y=self.line_no),
        ]
        next_line_adj_coordinates: list[Coordinates] = [
            Coordinates(x=x, y=self.line_no + 1)
            for x in range(self.start - 1, self.end + 2)
        ]
        return (
            previous_line_adj_coordinates
            + same_line_adj_coordinates
            + next_line_adj_coordinates
        )


def parse_single_line(line: str, line_no: int) -> list[PartNumber]:
    part_numbers: list[PartNumber] = []

    start: int | None = None
    number_str: str = ""
    max_idx = len(line) - 1

    def currently_in_digit_substring() -> bool:
        # We need to compare to None because a zero would
        # evaluate to False as well
        return start is not None

    def append_part_number_and_reset_vars(end: int):
        part_numbers.append(
            PartNumber(
                start=start,  # type: ignore
                end=end,
                line_no=line_no,
                number=int(number_str),
            )
        )

    for idx, char in enumerate(line):
        if char.isdigit():
            # Here we handle the case where the current digit is
            # the first digit of the number.
            if not currently_in_digit_substring():
                start = idx

            number_str += char

            # Here we handle the case where the current digit is
            # the last character of the line.
            if idx == max_idx:
                append_part_number_and_reset_vars(end=idx)
                start = None
                number_str = ""

        # Char is not a digit, but the previous char was.
        # This means that we have "moved out of" a digit-substring,
        # have to store the Partnumber and reset the temporary variables.
        elif currently_in_digit_substring():
            append_part_number_and_reset_vars(end=idx - 1)
            start = None
            number_str = ""

    return part_numbers


def parse_lines(lines: list[str]) -> list[PartNumber]:
    part_numbers: list[PartNumber] = []
    for y_idx, line in enumerate(lines):
        part_numbers.extend(parse_single_line(line, line_no=y_idx))

    return part_numbers


def is_symbol(char: str) -> bool:
    return not char.isdigit() and not char == "."


def has_adjacent_symbols(lines: list[str], part_number: PartNumber) -> bool:
    for coordinate in part_number.get_adj_coordinates():
        try:
            if is_symbol(lines[coordinate.y][coordinate.x]):
                return True
        except IndexError:
            continue
    return False


def part_1(filename: str):
    lines = get_lines(filename=filename)
    part_numbers = parse_lines(lines)
    total = 0
    for part_number in part_numbers:
        if has_adjacent_symbols(lines=lines, part_number=part_number):
            total += part_number.number

    return total


if __name__ == "__main__":
    print("Part 1:", part_1(INPUT))

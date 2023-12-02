from dataclasses import dataclass
from pathlib import Path

FILENAME = "input.txt"


@dataclass
class Game:
    id_: int
    draws: list[dict[str, int]]


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        lines = fh.readlines()
    return lines


def parse_line(line: str) -> Game:
    game_name, draws_string = line.split(":")

    _, game_id = game_name.split()
    game_id = int(game_id)

    draw_strings = draws_string.split(";")
    draws = [get_draw_from_string(draw_string) for draw_string in draw_strings]

    return Game(id_=game_id, draws=draws)


def get_draw_from_string(draw_string: str) -> dict[str, int]:
    count_colors = draw_string.strip().split(",")
    draw: dict[str, int] = {}
    for count_color in count_colors:
        count, color = count_color.split()
        draw[color] = int(count)
    return draw


def draws_are_possible(
    draws: list[dict[str, int]], given_cubes: dict[str, int]
) -> bool:
    maxima = get_color_maxima_from_draws(draws)

    for color, count in maxima.items():
        if count > given_cubes.get(color, 0):
            return False

    return True


def get_color_maxima_from_draws(draws: list[dict[str, int]]) -> dict[str, int]:
    maxima: dict[str, int] = {}
    for draw in draws:
        for color, count in draw.items():
            if count > maxima.get(color, 0):
                maxima[color] = count
    return maxima


def part_1():
    lines = get_lines(FILENAME)
    given_cubes = {"red": 12, "green": 13, "blue": 14}
    total = 0
    for line in lines:
        game = parse_line(line)
        if draws_are_possible(draws=game.draws, given_cubes=given_cubes):
            total += game.id_
    print("Part 1:", total)


### Part 2


def multiply_all(__list_of_ints: list[int]) -> int:
    if len(__list_of_ints) < 1:
        return 0

    product = 1
    for e in __list_of_ints:
        product *= e

    return product


def part_2():
    lines = get_lines(FILENAME)
    total = 0
    for line in lines:
        game = parse_line(line)
        maxima = get_color_maxima_from_draws(game.draws)
        power = multiply_all(list(maxima.values()))
        total += power
    print("Part 2:", total)


if __name__ == "__main__":
    part_1()
    part_2()

"""
answer_a: 14
"""

from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path

FILE = Path("input.real")


@dataclass(frozen=True)
class Location:
    x: int
    y: int


class Frequency(str):
    def __new__(cls, string: str):
        assert isinstance(string, str)
        assert len(string) == 1
        return super().__new__(cls, string)


@dataclass(frozen=True)
class Antenna:
    location: Location
    frequency: Frequency


Map = list[list[Frequency]]


upper_bound_x: int = 0
upper_bound_y: int = 0


def load_map() -> Map:
    with FILE.open(mode="r") as fh:
        map_ = [[Frequency(char) for char in line] for line in fh.read().splitlines()]

    global upper_bound_x
    global upper_bound_y
    upper_bound_x = len(map_[0])
    upper_bound_y = len(map_)

    return map_


def get_unique_frequencies(map_: Map) -> set[Frequency]:
    unique_frequencies = set(freq for row in map_ for freq in row)
    unique_frequencies.discard(Frequency("."))
    return unique_frequencies


def get_antennae(map_: Map) -> list[Antenna]:
    antennae: list[Antenna] = []

    for y, row in enumerate(map_):
        for x, freq in enumerate(row):
            if freq != ".":
                location = Location(x=x, y=y)
                antennae.append(Antenna(location=location, frequency=freq))

    return antennae


def get_frequency_to_antennae_map(
    antennae: list[Antenna],
) -> dict[Frequency, list[Antenna]]:
    f_to_a_map: dict[Frequency, list[Antenna]] = defaultdict(list)

    for a in antennae:
        f_to_a_map[a.frequency].append(a)

    return f_to_a_map


def get_antinodes_for_antennae_of_same_frequency(
    antennae: list[Antenna],
) -> set[Location]:

    antinodes: set[Location] = set()

    for antenna_pair in permutations(antennae, r=2):
        a_1, a_2 = antenna_pair
        location = Location(
            x=(2 * a_1.location.x) - a_2.location.x,
            y=(2 * a_1.location.y) - a_2.location.y,
        )

        x_ok = 0 <= location.x < upper_bound_x
        y_ok = 0 <= location.y < upper_bound_y
        if x_ok and y_ok:
            antinodes.add(location)

    return antinodes


def part_1() -> int:
    map_ = load_map()
    all_antennae = get_antennae(map_)
    antennae_by_frequency = get_frequency_to_antennae_map(all_antennae)

    antinodes: set[Location] = set()

    for antennae in antennae_by_frequency.values():
        antinodes.update(get_antinodes_for_antennae_of_same_frequency(antennae))

    return len(antinodes)


def get_antinodes_for_antennae_of_same_frequency_with_resonant_harmonics(
    antennae: list[Antenna],
) -> set[Location]:

    antinodes: set[Location] = set()

    for antenna_pair in permutations(antennae, r=2):
        a_1, a_2 = antenna_pair
        step_x = a_2.location.x - a_1.location.x
        step_y = a_2.location.y - a_1.location.y

        step_count = 0
        while True:
            location = Location(
                x=a_1.location.x + step_count * step_x,
                y=a_1.location.y + step_count * step_y,
            )

            x_ok = 0 <= location.x < upper_bound_x
            y_ok = 0 <= location.y < upper_bound_y
            if x_ok and y_ok:
                antinodes.add(location)
                step_count += 1
            else:
                break

    return antinodes


def part_2() -> int:
    map_ = load_map()
    all_antennae = get_antennae(map_)
    antennae_by_frequency = get_frequency_to_antennae_map(all_antennae)

    antinodes: set[Location] = set()

    for antennae in antennae_by_frequency.values():
        antinodes.update(
            get_antinodes_for_antennae_of_same_frequency_with_resonant_harmonics(
                antennae
            )
        )

    return len(antinodes)


if __name__ == "__main__":
    print(part_1())
    print(part_2())

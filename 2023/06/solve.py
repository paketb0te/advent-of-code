from dataclasses import dataclass, field
import itertools
from pathlib import Path
from typing import Iterable

INPUT = "input.txt"


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        return fh.read().splitlines()


@dataclass
class Race:
    time: int
    dist: int


def parse_lines(lines: list[str]) -> list[Race]:
    _, times_str = lines[0].split(":")
    times = [int(t) for t in times_str.split()]

    _, dists_str = lines[1].split(":")
    dists = [int(t) for t in dists_str.split()]

    return [Race(time=t, dist=d) for t, d in zip(times, dists)]


def get_possible_distances_for_time(time: int) -> Iterable[int]:
    dists: list[int] = []
    for i in range(time + 1):
        dist = i * (time - i)
        dists.append(dist)
    return (i * (time - i) for i in range(time + 1))


def get_count_of_winning_possibilities_for_race(race: Race) -> int:
    possible_distances = get_possible_distances_for_time(race.time)
    winning_distances = filter(lambda dist: dist > race.dist, possible_distances)
    return sum(1 for _ in winning_distances)


def part_1(filename: str) -> int:
    lines = get_lines(filename)
    races = parse_lines(lines)
    total = 1
    for race in races:
        total *= get_count_of_winning_possibilities_for_race(race)
    return total


### Part 2


def parse_lines_for_part_2(lines: list[str]) -> Race:
    _, time_str = lines[0].split(":")
    time = int(time_str.replace(" ", ""))

    _, dist_str = lines[1].split(":")
    dist = int(dist_str.replace(" ", ""))

    return Race(time=time, dist=dist)


def part_2(filename: str) -> int:
    lines = get_lines(filename)
    race = parse_lines_for_part_2(lines)

    return get_count_of_winning_possibilities_for_race(race)


if __name__ == "__main__":
    print("Part 1:", part_1(INPUT))
    print("Part 2:", part_2(INPUT))

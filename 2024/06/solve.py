from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from itertools import cycle

FILE = Path("input.real")


@dataclass(frozen=True)
class Location:
    x: int
    y: int


class Direction(Enum):
    # Enum values can be iterated over in order of definition
    # so we define them such an order that each direction is
    # a "right turn" from the previous one.
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"


@dataclass(frozen=True)
class VisitedLocation(Location):
    direction: Direction


class LoopError(Exception): ...


class LocationVisitor:
    def __init__(self, location: Location, direction: Direction):
        self._location = location
        self._directions_cycle = cycle(Direction)
        # "rotate" in the starting location until we face the correct direction
        while next(self._directions_cycle) != direction:
            continue
        self._direction = direction
        self._visited: set[VisitedLocation] = set()

    def get_current_location(self) -> Location:
        return self._location

    def get_next_location(self) -> Location:
        x = self._location.x
        y = self._location.y
        match self._direction:
            case Direction.UP:
                y -= 1
            case Direction.RIGHT:
                x += 1
            case Direction.DOWN:
                y += 1
            case Direction.LEFT:
                x -= 1
        return Location(x=x, y=y)

    def visit_location(self, location: Location) -> None:
        visited_location_new = VisitedLocation(
            x=location.x, y=location.y, direction=self.get_direction()
        )
        if visited_location_new in self.get_visited_locations():
            raise LoopError(f"Loop detected at {visited_location_new=}")

        self._visited.add(visited_location_new)
        self._location = location

    def get_visited_locations(self) -> set[VisitedLocation]:
        return self._visited

    def get_direction(self) -> Direction:
        return self._direction

    def update_direction(self) -> None:
        self._direction = next(self._directions_cycle)


def initialize_guard(_map: list[list[str]]) -> LocationVisitor:
    for y, line in enumerate(_map):
        for x, char in enumerate(line):
            if char in Direction:
                location = Location(x=x, y=y)
                direction = Direction(char)
                return LocationVisitor(location=location, direction=direction)

    raise ValueError("No guard found in map")


def load_map() -> list[list[str]]:
    _map: list[list[str]] = []
    with FILE.open(mode="r") as fh:
        for line in fh.read().splitlines():
            _map.append([char for char in line])
    return _map


def part_1(_map: list[list[str]]) -> int:
    # expected answer for test data: 41
    guard = initialize_guard(_map)
    X_UPPER_BOUND = len(_map[0])
    Y_UPPER_BOUND = len(_map)

    def _location_on_map(location: Location) -> bool:
        x_ok = 0 <= location.x < X_UPPER_BOUND
        y_ok = 0 <= location.y < Y_UPPER_BOUND
        return x_ok and y_ok

    while True:
        next_location = guard.get_next_location()
        if not _location_on_map(next_location):
            break
        if _map[next_location.y][next_location.x] == "#":
            guard.update_direction()
        else:
            guard.visit_location(next_location)
    return len(guard.get_visited_locations())


def part_2(_map: list[list[str]]) -> int:
    _map = load_map()

    locations_total = len(_map) * len(_map[0])

    loops_found = 0
    locations_count = 0
    for y, row in enumerate(_map):
        for x, char in enumerate(row):
            locations_count += 1
            print(f"{locations_count}/{locations_total}")
            original_char = char
            if char != ".":
                continue
            _map[y][x] = "#"
            try:
                part_1(_map)
            except LoopError:
                print(f"Loop found when placing obstacle at {x, y}")
                loops_found += 1
            _map[y][x] = original_char

    return loops_found


if __name__ == "__main__":
    _map = load_map()
    locations_visited = part_1(_map)
    print(f"The guard visited {locations_visited} Locations.")

    loops_found = part_2(_map)
    print(f"Found {loops_found} possible locations for obstacles that create a loop.")

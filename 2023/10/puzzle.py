import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Literal
from dataclasses import dataclass

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


type Symbol = Literal["|", "-", "L", "J", "7", "F", "S"]


@dataclass(frozen=True)
class Position:
    i: int
    j: int

    def __add__(self, other: "Position") -> "Position":
        return Position(i=self.i + other.i, j=self.j + other.j)


@dataclass
class Tile:
    symbol: Symbol
    pos: Position


SYMBOL_MAP: dict[Symbol, tuple[Position, Position]] = {
    "|": (Position(i=-1, j=0), Position(i=1, j=0)),
    "-": (Position(i=0, j=-1), Position(i=0, j=1)),
    "L": (Position(i=-1, j=0), Position(i=0, j=1)),
    "J": (Position(i=-1, j=0), Position(i=0, j=-1)),
    "7": (Position(i=1, j=0), Position(i=0, j=-1)),
    "F": (Position(i=1, j=0), Position(i=0, j=1)),
}


def get_next_position(current_tile: Tile, previous_tile: Tile) -> Position:
    a, b = SYMBOL_MAP[current_tile.symbol]
    possible_next_positions: set[Position] = set(
        (current_tile.pos + a, current_tile.pos + b)
    )

    next_step = possible_next_positions - set((previous_tile.pos,))
    next_step = next_step.pop()

    return next_step


def find_S(lines: list[str]) -> Tile:
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "S":
                pos = Position(i=i, j=j)
                return Tile(symbol="S", pos=pos)
    raise ValueError("S not found!")


def get_surrounding_positions(position: Position) -> Iterable[Position]:
    return [
        position + Position(i, j)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        if not i == j == 0
    ]


def get_starting_tile(lines: list[str]) -> Tile:
    s = find_S(lines=lines)

    for pos in get_surrounding_positions(s.pos):
        symbol: Symbol = lines[pos.i][pos.j]  # type: ignore
        try:
            a, b = SYMBOL_MAP[symbol]
        except KeyError:
            continue
        if s.pos in (pos + a, pos + b):
            return Tile(symbol=symbol, pos=pos)

    raise ValueError("No pipes matching S!")


def get_tile_from_pos(lines: list[str], pos: Position) -> Tile:
    return Tile(symbol=lines[pos.i][pos.j], pos=pos)  # type: ignore


def solve_part_1(filename: str) -> int:
    lines = get_lines(filename)
    s = find_S(lines)
    current_tile = get_starting_tile(lines=lines)
    total = 1  # Start with 1, because we start not at S but at the first pipe already
    previous_tile = s
    while current_tile != s:
        total += 1
        next_pos = get_next_position(
            current_tile=current_tile, previous_tile=previous_tile
        )
        previous_tile = current_tile
        current_tile = get_tile_from_pos(lines, next_pos)

    return int(total / 2)


if __name__ == "__main__":
    with timer():
        print("Part 1:", solve_part_1(INPUT))
    # with timer():
    #     print("Part 2:", solve_part_2(INPUT))
    ...

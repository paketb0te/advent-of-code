from dataclasses import dataclass
from pathlib import Path

INPUT = "input.txt"


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        return fh.read().splitlines()


@dataclass
class MapEntry:
    dst_start: int
    src_start: int
    range_length: int

    def map(self, src: int) -> int:
        if not self._value_in_range(src):
            raise ValueError(
                f"src out of bounds: {self.src_start=} {self.range_length=}"
            )
        offset = self.dst_start - self.src_start
        return src + offset

    def _value_in_range(self, value: int) -> bool:
        return self.src_start <= value <= self.src_start + self.range_length - 1


def parse_mapping_name(line: str) -> tuple[str, str]:
    name, _ = line.split()
    src_name, _, dst_name = name.split("-")
    return src_name, dst_name


def parse_seeds(line: str) -> list[int]:
    _, seeds = line.split(":")
    return [int(n) for n in seeds.split()]


def parse_map_line(line: str) -> MapEntry:
    dst_start, src_start, range_length = line.split()
    return MapEntry(
        dst_start=int(dst_start),
        src_start=int(src_start),
        range_length=int(range_length),
    )


if __name__ == "__main__":
    ...
    # print("Part 1:", part_1(INPUT))
    # print("Part 2:", part_2(INPUT))

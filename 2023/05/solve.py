import itertools
from dataclasses import dataclass, field
from pathlib import Path

INPUT = "input.txt"


def get_lines(filename: str) -> list[str]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        return fh.read().splitlines()


@dataclass(frozen=True)
class MapEntry:
    dst_start: int
    src_start: int
    range_length: int

    def map(self, value: int) -> int:
        if not self.value_in_range(value):
            raise ValueError(
                f"src out of bounds: {self.src_start=} {self.range_length=}"
            )
        return value + self.offset

    def value_in_range(self, value: int) -> bool:
        return self.src_start <= value <= self.src_start + self.range_length - 1

    @property
    def range(self) -> range:
        return range(self.src_start, self.src_start + self.range_length)

    @property
    def offset(self) -> int:
        return self.dst_start - self.src_start


@dataclass()
class Map:
    source: str
    target: str
    entries: list[MapEntry] = field(default_factory=list)

    def map(self, value: int) -> int:
        for entry in self.entries:
            if entry.value_in_range(value):
                return entry.map(value)
        return value


def parse_mapping_name(line: str) -> tuple[str, str]:
    name, _ = line.split()
    src_name, _, dst_name = name.split("-")
    return src_name, dst_name


def parse_seeds(line: str) -> list[int]:
    _, seeds = line.split(":")
    return [int(n) for n in seeds.split()]


def parse_map_entry_line(line: str) -> MapEntry:
    dst_start, src_start, range_length = line.split()
    return MapEntry(
        dst_start=int(dst_start),
        src_start=int(src_start),
        range_length=int(range_length),
    )


def build_maps_from_lines(lines: list[str]) -> list[Map]:
    maps: list[Map] = []

    current_map: Map | None = None
    current_entry: MapEntry | None = None
    current_entries: list[MapEntry] = []

    for line in lines:
        if line.endswith("map:"):
            source, target = parse_mapping_name(line)
            current_map = Map(source=source, target=target)
        elif line == "" and current_map is not None:
            current_map.entries = sorted(current_entries, key=lambda x: x.src_start)
            maps.append(current_map)
            current_entries = []
            current_map = None
        else:
            current_entry = parse_map_entry_line(line)
            current_entries.append(current_entry)

    return maps


def calculate(value: int, maps: list[Map]) -> int:
    for m in maps:
        value = m.map(value)
    return value


def part_1(filename: str):
    lines = get_lines(filename)
    seeds = parse_seeds(line=lines[0])

    # Append an empty line so the loop in
    # build_maps_from_lines() recognizes the last Map
    lines.append("")

    maps = build_maps_from_lines(lines=lines[2:])

    locations: list[int] = []
    for seed in seeds:
        location = calculate(value=seed, maps=maps)
        locations.append(location)

    return min(locations)


### Part 2


def parse_seeds_as_ranges(line: str) -> list[range]:
    values = parse_seeds(line)
    return [
        range(start, start + length) for start, length in itertools.batched(values, 2)
    ]


def map_range_to_ranges(range_: range, map: Map) -> list[range]:
    ranges: list[range] = []

    start = range_[0]
    end = range_[-1]

    for entry in map.entries:
        if start < entry.range[0]:
            if end < entry.range[0]:
                ranges.append(range(start, end + 1))
                break

            elif entry.range[0] <= end <= entry.range[-1]:
                ranges.append(range(start, entry.range[0]))
                ranges.append(
                    range(entry.range[0] + entry.offset, end + entry.offset + 1)
                )
                break

            elif entry.range[-1] < end:
                ranges.append(range(start, entry.range[0]))
                ranges.append(
                    range(
                        entry.range[0] + entry.offset,
                        entry.range[-1] + entry.offset + 1,
                    )
                )
                start = entry.range[-1]

        elif entry.range[0] <= start <= entry.range[-1]:
            if end < entry.range[0]:
                raise ValueError("end lower than start")

            elif entry.range[0] <= end <= entry.range[-1]:
                r = range(start + entry.offset, end + entry.offset + 1)
                ranges.append(r)
                break

            elif entry.range[-1 < end]:
                r = range(start + entry.offset, entry.range[-1] + entry.offset + 1)
                ranges.append(r)
                start = entry.range[-1] + 1

        elif entry.range[-1] < start:
            continue

    else:
        ranges.append(range(start, end + 1))

    return ranges


def map_ranges_to_ranges(ranges: list[range], map: Map) -> list[range]:
    return_ranges: list[range] = []
    for r in ranges:
        return_ranges += map_range_to_ranges(r, map)

    return return_ranges


def part_2(filename: str):
    lines = get_lines(filename)
    seed_ranges = parse_seeds_as_ranges(line=lines[0])

    # Append an empty line so the loop in
    # build_maps_from_lines() recognizes the last Map
    lines.append("")

    maps = build_maps_from_lines(lines=lines[2:])

    ranges = seed_ranges
    for m in maps:
        ranges = map_ranges_to_ranges(ranges, m)

    return min(r[0] for r in ranges)


if __name__ == "__main__":
    print("Part 1:", part_1(INPUT))
    print("Part 2:", part_2(INPUT))

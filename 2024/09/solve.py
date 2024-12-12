"""
answer_a: 1928
"""

import argparse
from collections import deque
from pathlib import Path
from typing import Iterable

FILE = Path("input.real")

DiskMap = list[int | None]


def load_disk_map(file: Path) -> DiskMap:

    with file.open(mode="r") as fh:
        string = fh.read().strip()

    disk_map: DiskMap = []
    for idx, char in enumerate(string):
        if idx % 2 == 0:
            # because only eveery _other_ element represents a file,
            # the file_id is idx/2
            file_id = int(idx / 2)
        else:
            # the file_id is None for empty blocks
            file_id = None

        for _ in range(int(char)):
            disk_map.append(file_id)

    return disk_map


def part_1(file: Path) -> int:
    disk_map: DiskMap = load_disk_map(file)
    queue = deque(disk_map)
    compacted_map: list[int] = []
    while queue:
        block = queue.popleft()
        if block is None:
            last_nonempty_block = None
            while queue and last_nonempty_block is None:
                last_nonempty_block = queue.pop()
            if last_nonempty_block is not None:
                compacted_map.append(last_nonempty_block)

        else:
            compacted_map.append(block)

    checksum: int = sum(idx * file_id for idx, file_id in enumerate(compacted_map))

    return checksum


def part_2(file: Path) -> int: ...


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("filename")
    args = p.parse_args()
    file = Path(args.filename)
    print(part_1(file))
    print(part_2(file))

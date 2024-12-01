from pathlib import Path
from collections import Counter

FILE = Path("input.txt")


def get_lists(file: Path) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []

    with file.open(mode="r") as fh:
        for line in fh:
            values = line.split(maxsplit=1)
            left.append(int(values[0]))
            right.append(int(values[1]))

    left.sort()
    right.sort()

    return left, right


def part_1(left: list[int], right: list[int]) -> int:
    total = 0
    for l, r in zip(left, right):
        total += abs(l - r)
    return total


def part_2(left: list[int], right: list[int]) -> int:
    total = 0
    right_counter = Counter(right)
    for element in left:
        total += element * right_counter.get(element, 0)
    return total


def main() -> None:
    left, right = get_lists(FILE)
    print(part_1(left=left, right=right))
    print(part_2(left=left, right=right))


if __name__ == "__main__":
    main()

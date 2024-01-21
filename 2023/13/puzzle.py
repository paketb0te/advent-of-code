from pprint import pprint
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable


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


def get_patterns(filename: str) -> Iterable[list[str]]:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        patterns = fh.read().split("\n\n")

    for p in patterns:
        yield p.splitlines()


def find_number_of_columns(pattern: list[str]) -> int | None:
    for column in range(1, len(pattern[0]) - 1):
        for line in pattern:
            left = line[:column]
            right = line[column:]
            print(left, "|", right)
            left = "".join(reversed(left))
            x = zip(left, right)
            if any(a != b for a, b in x):
                break
            return column


def find_number_of_rows(pattern: list[str]) -> int | None:
    for mirror_line in range(len(pattern)):
        print(mirror_line)
        upper = pattern[:mirror_line]
        lower = pattern[mirror_line:]
        # upper = reversed(upper)
        for x in upper:
            print(x)
        print("-" * 10)
        for x in lower:
            print(x)
        x = zip(upper, lower)
        # for a, b in x:
        #     print(a)
        #     print(b)
        # if any(a != b for a, b in x):
        #     break
        # return mirror_line
        # if pattern[mirror_line] == pattern
        # for line in pattern:
        #     left = line[:column]
        #     right = line[column:]
        #     print(left, "|", right)
        #     left = "".join(reversed(left))
        #     x = zip(left, right)
        #     if any(a != b for a, b in x):
        #         break
        #     return column


if __name__ == "__main__":
    for p in get_patterns(INPUT):
        pprint(p)
    # with timer():
    #     print("Part 1:", get_patterns(INPUT))
#     with timer():
#         print("Part 2:", solve(INPUT, space_factor=1_000_000))

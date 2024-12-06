import re
from pathlib import Path
from pprint import pprint

FILE = Path("input.test")
XMAS = re.compile(r"XMAS")


def load_file(path: Path = FILE) -> list[list[str]]:
    with path.open(mode="r") as fh:
        return [[char for char in line.strip()] for line in fh.readlines()]


def rotate_left(matrix: list[list[str]]) -> list[list[str]]:
    result = [["_" for _ in range(len(matrix))] for _ in range(len(matrix[0]))]

    # "transpose" the matrix
    for i, row in enumerate(matrix):
        for j, char in enumerate(row):
            result[j][i] = char

    # "mirror" the matrix
    result = result[::-1]

    # the combination of transposing and mirroring results in a rotation
    return result


def part_1():
    total = 0
    matrix = load_file()
    for _ in range(4):
        matrix = rotate_left(matrix)
        print("=" * 80)
        pprint(matrix)
        total += get_horizontal_matches(matrix)

    print(total)


def get_horizontal_matches(matrix: list[list[str]]) -> int:
    return sum(len(re.findall(XMAS, "".join(row))) for row in matrix)


def get_diagonal_matches(matrix: list[list[str]]) -> int:
    lines = list[str]
    for i, char in enumerate(matrix[0]):
        for j, _ in enumerate(matrix):
            lines.append("".join(matrix[i][j]))

    total = 0


if __name__ == "__main__":
    part_1()

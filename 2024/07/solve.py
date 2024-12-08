"""
answer_a: 3749
"""

from itertools import product
from pathlib import Path
from typing import Callable, Iterable

FILE = Path("input.real")


Equation = tuple[int, list[int]]
Operator = Callable[[int, int], int]


def load_equations():

    equations: Iterable[Equation] = []

    with FILE.open(mode="r") as fh:
        for line in fh.read().splitlines():
            left, right = line.split(":", maxsplit=1)
            value = int(left)
            numbers = [int(n) for n in right.split()]
            equations.append((value, numbers))

    return equations


def solve(equations: Iterable[Equation], operators: Iterable[Operator]) -> int:
    total = 0
    for equation in equations:
        value, numbers = equation
        operator_permutations = product(operators, repeat=len(numbers) - 1)
        if any(
            fold_numbers_and_operators(numbers, operators) == value
            for operators in operator_permutations
        ):
            total += value

    return total


def add(a: int, b: int) -> int:
    return a + b


def mul(a: int, b: int) -> int:
    return a * b


def concat(a: int, b: int) -> int:
    c = str(a) + str(b)
    return int(c)


def fold_numbers_and_operators(
    numbers: list[int], operators: Iterable[Operator]
) -> int:
    total = numbers[0]
    for operator, number in zip(operators, numbers[1:]):
        total = operator(total, number)
    return total


if __name__ == "__main__":
    equations = load_equations()
    operators = [add, mul]
    # part 1:
    print(solve(equations, operators))
    # part 2:
    operators.append(concat)
    print(solve(equations, operators))

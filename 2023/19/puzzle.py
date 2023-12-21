import operator
import re
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol

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


PART_MATCHING_PATTERN = re.compile(r"^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$")
WORKFLOW_MATCHING_PATTERN = re.compile(r"^(\w+){(.*)}$")
RULE_MATCHING_PATTERN = re.compile(r"^([xmas])([<>])(\d+):(\w+)$")

OPERATOR_MAP = {"<": operator.lt, ">": operator.gt}


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def all_ratings(self) -> int:
        return self.x + self.m + self.a + self.s


type Rule = Callable[[Part], bool]


class Runnable(Protocol):
    def run(self, part: Part) -> None:
        ...


def parse_part_line(line: str) -> Part:
    matches = re.findall(PART_MATCHING_PATTERN, line)[0]
    x, m, a, s = (int(value) for value in matches)
    return Part(x=x, m=m, a=a, s=s)


def parse_rule(rule_string: str) -> Rule:
    attr_name, operator_sign, value, next_workflow_name = re.findall(
        RULE_MATCHING_PATTERN, rule_string
    )[0]

    attr_name: str = attr_name
    operator_sign: str = operator_sign
    value: int = int(value)
    next_workflow_name: str = next_workflow_name

    compare = OPERATOR_MAP[operator_sign]

    def rule(part: Part) -> bool:
        attr = getattr(part, attr_name)
        rule_matches = False
        if compare(attr, value):
            WORKFLOW_MAP[next_workflow_name].run(part=part)
            rule_matches = True
        return rule_matches

    return rule


class Workflow:
    def __init__(self, line: str) -> None:
        name, rules = re.findall(WORKFLOW_MATCHING_PATTERN, line)[0]

        rule_strings: list[str] = rules.split(",")
        default_workflow_name = rule_strings[-1]

        def default_rule(part: Part) -> bool:
            WORKFLOW_MAP[default_workflow_name].run(part)
            return True

        self.rules: list[Rule] = [parse_rule(rule) for rule in rule_strings[:-1]]
        self.rules.append(default_rule)

        WORKFLOW_MAP[name] = self

    def run(self, part: Part) -> None:
        for rule in self.rules:
            if rule(part):
                break


class Accept:
    def run(self, part: Part) -> None:
        ACCEPTED_PARTS.append(part)


class Reject:
    def run(self, part: Part) -> None:
        REJECTED_PARTS.append(part)


ACCEPTED_PARTS: list[Part] = []
REJECTED_PARTS: list[Part] = []
WORKFLOW_MAP: dict[str, Runnable] = {"A": Accept(), "R": Reject()}


def solve_part_1(filename: str) -> int:
    file = Path(__file__).parent / filename
    with file.open("r") as fh:
        content = fh.read()
        workflows_block, parts_block = content.split("\n\n", maxsplit=1)

    workflow_lines = workflows_block.splitlines()
    part_lines = parts_block.splitlines()

    for line in workflow_lines:
        Workflow(line)

    parts: list[Part] = [parse_part_line(line) for line in part_lines]
    for part in parts:
        WORKFLOW_MAP["in"].run(part)

    return sum(part.all_ratings() for part in ACCEPTED_PARTS)


if __name__ == "__main__":
    ...
    with timer():
        print("Part 1:", solve_part_1(INPUT))
    # with timer():
    #     print("Part 2:", solve_part_2(INPUT))

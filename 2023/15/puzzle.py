import re
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

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


def hash(string: str) -> int:
    """
    To run the HASH algorithm on a string, start with a current value of 0.
    Then, for each character in the string starting from the beginning:

    - Determine the ASCII code for the current character of the string.
    - Increase the current value by the ASCII code you just determined.
    - Set the current value to itself multiplied by 17.
    - Set the current value to the remainder of dividing itself by 256.

    After following these steps for each character in the string in order,
    the current value is the output of the HASH algorithm.
    """
    FACTOR = 17
    RANGE = 256

    current_value = 0

    for char in string:
        ascii_code = ord(char)
        current_value += ascii_code
        current_value *= FACTOR
        current_value = current_value % RANGE

    return current_value


def solve_part_1(filename: str) -> int:
    # There is only one line of imput
    line = get_lines(filename)[0]
    steps = line.split(",")

    return sum(hash(step) for step in steps)


### Part 2


type Operation = Literal["=", "-"]
type Box = dict[str, int]

STEP_EXPR = re.compile(r"^([\w]*)([=|-])([\d]?)$")


@dataclass
class Step:
    label: str
    operation: Operation
    focal_length: int | None


def parse_step(step_string: str) -> Step:
    groups = re.findall(STEP_EXPR, step_string)[0]
    label: str = groups[0]
    operation: Operation = groups[1]
    try:
        focal_length = int(groups[2])
    except ValueError:
        focal_length = None

    return Step(label=label, operation=operation, focal_length=focal_length)


def solve_part_2(filename: str) -> int:
    # There is only one line of imput
    line = get_lines(filename)[0]
    steps = line.split(",")
    boxes = build_boxes(steps)
    total = 0
    for box_num, box in boxes.items():
        for slot, focal_length in enumerate(box.values(), start=1):
            total += (box_num + 1) * slot * focal_length
    return total


def build_boxes(steps: list[str]) -> dict[int, Box]:
    boxes: dict[int, Box] = {}

    for step_str in steps:
        step = parse_step(step_str)
        label_hash = hash(step.label)
        box: Box = boxes.get(label_hash, {})

        match step.operation:
            case "=":
                if not step.focal_length:
                    raise ValueError(f"Operation '=' requires focal_length!")
                box[step.label] = step.focal_length
            case "-":
                box.pop(step.label, None)

        boxes[label_hash] = box

    return boxes


if __name__ == "__main__":
    ...
    with timer():
        print("Part 1:", solve_part_1(INPUT))
    with timer():
        print("Part 2:", solve_part_2(INPUT))

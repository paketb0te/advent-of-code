import re
from pathlib import Path


FILE = Path("input.real")

MUL_REGEX_WITH_CAPTURE = r"mul\((\d+),(\d+)\)"


def part_1():
    with FILE.open(mode="r") as fh:
        instructions = fh.read()
        total = sum(
            int(match[0]) * int(match[1])
            for match in re.findall(MUL_REGEX_WITH_CAPTURE, instructions)
        )
    print(total)


MUL_REGEX = r"mul\(\d+,\d+\)"
DO_REGEX = r"do\(\)"
DONT_REGEX = r"don't\(\)"


def part_2():
    total = 0
    with FILE.open(mode="r") as fh:
        instructions_enabled = True
        instructions = fh.read()
        for match in re.findall(f"{MUL_REGEX}|{DO_REGEX}|{DONT_REGEX}", instructions):
            if re.match(DO_REGEX, match):
                instructions_enabled = True
            elif re.match(DONT_REGEX, match):
                instructions_enabled = False
            elif m := re.match(MUL_REGEX_WITH_CAPTURE, match).groups():
                if instructions_enabled:
                    total += int(m[0]) * int(m[1])
            else:
                raise

    print(total)


if __name__ == "__main__":
    part_1()
    part_2()

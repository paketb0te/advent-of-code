from pathlib import Path

FILE = Path("input.real")


def report_is_safe(report: list[int]) -> bool:
    if report[0] < report[1]:
        increasing = True
    elif report[0] > report[1]:
        increasing = False
    else:
        # If they are the same, the record is not safe by definition
        # and we do not need to evaluate further
        return False

    current = report[0]
    for level in report[1:]:
        difference = level - current
        current = level

        if increasing:
            if not (0 < difference <= 3):
                return False
        else:
            if not (-3 <= difference < 0):
                return False

    return True


def part_1():
    with FILE.open(mode="r") as fh:
        safe_reports_count = 0

        for line in fh:
            report = [int(level) for level in line.split()]

            if report_is_safe(report=report):
                safe_reports_count += 1

    print(safe_reports_count)


if __name__ == "__main__":
    part_1()

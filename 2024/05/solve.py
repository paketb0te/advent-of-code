from dataclasses import dataclass
from pathlib import Path

FILE = Path("input.real")


@dataclass(frozen=True)
class Rule:
    number_lower: int
    number_higher: int


rules: set[Rule]


class Page:
    def __init__(self, number: int):
        self.number = number

    def __lt__(self, other: "Page"):
        return Rule(number_lower=self.number, number_higher=other.number) in rules


Update = list[Page]


def load_rules_and_get_updates(
    path: Path = FILE,
) -> list[Update]:

    with path.open(mode="r") as fh:
        global rules
        rules = set()
        while line := fh.readline().strip():
            # The blank line marks the end of rules / start of updates
            if not line:
                break
            elements = line.split("|", maxsplit=1)
            rules.add(Rule(int(elements[0]), int(elements[1])))

        updates: list[Update] = []
        while line := fh.readline().strip():
            updates.append([Page(int(i)) for i in line.split(",")])

    return updates


def update_conforms_to_rules(update: Update) -> bool:
    return update == sorted(update)


def part_1(updates: list[Update]):
    global rules
    total = 0
    for update in updates:
        if update_conforms_to_rules(update):
            middle_index = int(len(update) / 2)
            total += update[middle_index].number
    return total


def part_2(updates: list[Update]):
    total = 0
    for update in updates:
        if not update_conforms_to_rules(update):
            middle_index = int(len(update) / 2)
            total += sorted(update)[middle_index].number
    return total


if __name__ == "__main__":
    updates = load_rules_and_get_updates()
    print(part_1(updates))
    print(part_2(updates))

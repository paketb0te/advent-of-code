"""
answer_a: 36
"""

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator


@dataclass(frozen=True)
class Postition:
    i: int
    j: int


@dataclass
class Node:
    pos: Postition
    value: int
    children: list["Node"] = field(default_factory=list)


def load_map(file: Path) -> list[list[int]]:
    map_: list[list[int]] = []
    with file.open(mode="r") as fh:
        for line in fh:
            map_.append([int(char) for char in line.strip()])

    return map_


def get_child_nodes(curr_pos: Postition, map_: list[list[int]]) -> list[Node]:

    up = Postition(i=curr_pos.i - 1, j=curr_pos.j)
    down = Postition(i=curr_pos.i + 1, j=curr_pos.j)
    left = Postition(i=curr_pos.i, j=curr_pos.j - 1)
    right = Postition(i=curr_pos.i, j=curr_pos.j + 1)

    next_positions: list[Node] = []
    for pos in up, down, left, right:
        i_ok = 0 <= pos.i < len(map_)
        j_ok = 0 <= pos.j < len(map_[0])
        try:
            height_ok = map_[pos.i][pos.j] == (map_[curr_pos.i][curr_pos.j] + 1)
        except IndexError:
            height_ok = False

        if i_ok and j_ok and height_ok:
            next_positions.append(
                Node(
                    pos=pos,
                    value=map_[pos.i][pos.j],
                    children=get_child_nodes(curr_pos=pos, map_=map_),
                )
            )

    return next_positions


def part_1(file: Path) -> int:
    map_ = load_map(file)

    total_score = 0
    for i, line in enumerate(map_):
        for j, height in enumerate(line):
            if height == 0:
                pos = Postition(i=i, j=j)
                total_score += calculate_score_for_trailhead(pos=pos, map_=map_)

    return total_score


def get_leaf_nodes(node: Node) -> Generator[Node, Any, None]:
    if not node.children:
        yield node
    else:
        for child in node.children:
            yield from get_leaf_nodes(child)


def calculate_score_for_trailhead(pos: Postition, map_: list[list[int]]):
    root = Node(
        pos=pos,
        value=map_[pos.i][pos.j],
        children=get_child_nodes(curr_pos=pos, map_=map_),
    )
    score = len({leaf.pos for leaf in get_leaf_nodes(root) if leaf.value == 9})

    return score


def part_2(file: Path) -> int: ...


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("filename")
    args = p.parse_args()
    file = Path(args.filename)
    print(part_1(file))
    print(part_2(file))

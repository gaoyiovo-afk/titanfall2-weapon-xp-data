#!/usr/bin/env python3
"""Calculate minimum cumulative Titanfall 2 weapon XP for a displayed rank."""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEVEL_TABLE = ROOT / "data" / "xp_per_weapon_level.csv"
WEAPON_TABLE = ROOT / "data" / "weapon_xp_types.csv"


@dataclass(frozen=True)
class Result:
    weapon: str
    item_ref: str
    displayed_rank: str
    generation: int
    displayed_level: int
    internal_level: int
    xp_type: str
    xp_per_generation: int
    xp_into_current_generation: int
    minimum_cumulative_weapon_xp: int
    maximum_xp_before_next_displayed_rank: int


def load_level_table(path: Path = LEVEL_TABLE) -> list[dict[str, int]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = [
            {key: int(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]
    if len(rows) != 20 or [row["level"] for row in rows] != list(range(1, 21)):
        raise ValueError("Expected exactly levels 1 through 20")
    return rows


def load_weapons(path: Path = WEAPON_TABLE) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    lookup: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        names = [row["weapon"], row["itemRef"], *row["aliases"].split("|")]
        for name in names:
            lookup[name.strip().casefold()] = row
    return lookup, rows


def parse_rank(text: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*[gG]?(\d+)\.(\d+)\s*", text)
    if not match:
        raise ValueError("Rank must look like G25.2 or 25.2")
    generation, displayed_level = map(int, match.groups())
    if generation < 1 or generation > 99:
        raise ValueError("Generation must be between 1 and 99")
    if generation == 1 and not 1 <= displayed_level <= 20:
        raise ValueError("Generation 1 displays levels 1 through 20")
    if generation > 1 and not 0 <= displayed_level <= 19:
        raise ValueError("Generation 2+ displays sublevels 0 through 19")
    return generation, displayed_level


def calculate(weapon_name: str, rank: str) -> Result:
    levels = load_level_table()
    lookup, _ = load_weapons()
    try:
        weapon = lookup[weapon_name.strip().casefold()]
    except KeyError as exc:
        supported = ", ".join(sorted({row["weapon"] for row in lookup.values()}))
        raise ValueError(f"Unknown weapon {weapon_name!r}. Supported: {supported}") from exc

    generation, displayed_level = parse_rank(rank)
    xp_type = weapon["xpPerLevelType"]
    pips = [row[xp_type] for row in levels]
    xp_per_generation = sum(pips)

    if generation == 1:
        internal_level = displayed_level
        completed_rows = displayed_level - 1
    else:
        internal_level = displayed_level + 1
        completed_rows = displayed_level

    xp_into_generation = sum(pips[:completed_rows])
    minimum = (generation - 1) * xp_per_generation + xp_into_generation
    current_level_cost = pips[internal_level - 1]
    maximum = minimum + current_level_cost - 1

    return Result(
        weapon=weapon["weapon"],
        item_ref=weapon["itemRef"],
        displayed_rank=(
            str(displayed_level)
            if generation == 1
            else f"G{generation}.{displayed_level}"
        ),
        generation=generation,
        displayed_level=displayed_level,
        internal_level=internal_level,
        xp_type=xp_type,
        xp_per_generation=xp_per_generation,
        xp_into_current_generation=xp_into_generation,
        minimum_cumulative_weapon_xp=minimum,
        maximum_xp_before_next_displayed_rank=maximum,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate Titanfall 2 weapon XP from a displayed Generation/Level."
    )
    parser.add_argument("weapon", help="Weapon name, alias, or internal itemRef")
    parser.add_argument("rank", help="Displayed rank, for example G25.2 or 25.2")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    try:
        result = calculate(args.weapon, args.rank)
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        return

    print(f"Weapon: {result.weapon}")
    print(f"Internal itemRef: {result.item_ref}")
    print(f"Displayed rank: {result.displayed_rank}")
    print(f"XP type: {result.xp_type}")
    print(f"XP per Generation: {result.xp_per_generation}")
    print(f"XP into current Generation: {result.xp_into_current_generation}")
    print(f"Minimum cumulative weapon XP: {result.minimum_cumulative_weapon_xp}")
    print(
        "Possible XP range at this displayed rank: "
        f"{result.minimum_cumulative_weapon_xp}-"
        f"{result.maximum_xp_before_next_displayed_rank}"
    )


if __name__ == "__main__":
    main()

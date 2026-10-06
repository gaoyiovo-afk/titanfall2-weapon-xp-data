# Titanfall 2 Weapon XP / Generation Progression Data

[中文说明](README.zh-CN.md)

Verified progression data and formulas for **Titanfall 2 weapon XP**, including the original `xp_per_weapon_level` table, `xpPerLevelType` mappings, Generation totals, and a small calculator.

Useful search terms: Titanfall 2 weapon XP, weapon generation, weapon regeneration, Northstar progression, `xp_per_weapon_level.rpak`, `pilot_weapons.rpak`, `WeaponGetMaxXPPerGen`, `WeaponGetGenForXP`, and `WeaponGetLevelForXP`.

## Key findings

Titanfall 2 does **not** use a universal “200 kills per weapon Generation” rule. The amount depends on the weapon's `xpPerLevelType`:

| xpPerLevelType | XP/pips per complete Generation |
|---|---:|
| `default` | **185** |
| `sniper` | **94** |
| `pistol` | **94** |
| `antititan` | **77** |

These are weapon XP/pips, not a guaranteed count of final kills. Score-event multipliers, Titan/Auto-Titan elimination events, custom servers, and hidden progress inside the current displayed level can make kill counts differ.

## Original level table

The verified asset path is `datatable/xp_per_weapon_level.rpak`, whose RTech GUID is `0x5FFC5DAB7723E105`.

| Level | default | sniper | pistol | antititan |
|---:|---:|---:|---:|---:|
| 1 | 3 | 2 | 2 | 2 |
| 2 | 5 | 3 | 3 | 3 |
| 3 | 7 | 4 | 4 | 4 |
| 4–20, each | 10 | 5 | 5 | 4 |

The uncompressed 20-row table is available at [`data/xp_per_weapon_level.csv`](data/xp_per_weapon_level.csv).

## Display-level formula

For a type `t`, let:

```text
C_t(k) = sum of rows 1 through k
T_t    = C_t(20), the XP for one complete Generation
```

The original display code subtracts one from the internal weapon level after Generation 1. Therefore, for a displayed rank `Gg.s` where `g > 1`:

```text
minimum cumulative weapon XP = (g - 1) × T_t + C_t(s)
```

This means the exact Generation boundary is displayed as `G2.0`, `G3.0`, and so on. For example, CAR `G25.2` corresponds to internal level 3:

```text
24 × 185 + (3 + 5) = 4,448 minimum weapon XP
```

## Verified weapon mappings

| Weapon | Internal itemRef | xpPerLevelType |
|---|---|---|
| CAR | `mp_weapon_car` | `default` |
| R-97 | `mp_weapon_r97` | `default` |
| Volt | `mp_weapon_hemlok_smg` | `default` |
| Longbow DMR | `mp_weapon_sniper` | `sniper` |
| EVA-8 | `mp_weapon_shotgun` | `default` |
| SMR | `mp_weapon_smr` | `default` |
| EPG | `mp_weapon_epg` | `default` |
| Wingman Elite | `mp_weapon_wingman_n` | `default` |
| RE-45 | `mp_weapon_semipistol` | `pistol` |
| Charge Rifle | `mp_weapon_defender` | `antititan` |
| Thunderbolt | `mp_weapon_arc_launcher` | `antititan` |
| Archer | `mp_weapon_rocket_launcher` | `antititan` |

The machine-readable mapping is in [`data/weapon_xp_types.csv`](data/weapon_xp_types.csv).

## Calculator

Python 3 is sufficient; no third-party packages are required.

```console
python tools/calculate_weapon_xp.py CAR G25.2
python tools/calculate_weapon_xp.py "Wingman Elite" G3.6
python tools/calculate_weapon_xp.py 雷电球 38.8 --json
```

Example output:

```text
Weapon: CAR
Displayed rank: G25.2
XP type: default
XP per Generation: 185
Minimum cumulative weapon XP: 4448
Possible XP range at this displayed rank: 4448-4454
```

Run the tests with:

```console
python -m unittest discover -s tests -v
```

## Repository contents

- `data/xp_per_weapon_level.csv` — complete 20-row progression table.
- `data/weapon_xp_types.csv` — verified weapon-to-column mappings and aliases.
- `data/xp_type_totals.csv` — one-Generation totals.
- `examples/weapon_xp_example.csv` — worked example for 12 weapons.
- `tools/calculate_weapon_xp.py` — dependency-free calculator.
- `docs/methodology.md` — extraction, asset identity, formulas, and validation method.
- `NOTICE.md` — attribution and redistribution boundary.

## Reproducibility and sources

The RPAK tables were extracted from a locally installed copy of Titanfall 2 using [RSX](https://github.com/r-ex/rsx) 2.3.0. VPK script inspection used [tf2vpk](https://github.com/pg9182/tf2vpk). Asset identity was independently checked with RSX's `RTech::StringToGuid` implementation.

This repository deliberately does **not** redistribute Titanfall 2 RPAK/VPK containers, full proprietary game scripts, or extractor binaries. See [`docs/methodology.md`](docs/methodology.md) for the audit trail.

## License and disclaimer

The original code and documentation in this repository are licensed under the MIT License. Titanfall, Titanfall 2, Respawn, and related names and game assets belong to their respective owners. This is an unofficial community research project and is not affiliated with or endorsed by Electronic Arts, Respawn Entertainment, or the Northstar project.

Small factual tables and derived calculations are provided for research and verification. If you own the game, you can reproduce the extraction by following the methodology instead of relying on redistributed game assets.

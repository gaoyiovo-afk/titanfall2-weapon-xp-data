# Extraction and validation methodology

## Scope

The source installation was opened read-only. No Titanfall 2 game file, save, or Northstar data file was modified. Temporary extraction data was kept outside the game directory and removed after verification.

This public repository contains only small factual tables, derived calculations, original documentation, and an original calculator. It does not contain RPAK/VPK containers, full game scripts, or extractor executables.

## Tools

- [RSX 2.3.0](https://github.com/r-ex/rsx), AGPL-3.0, was used to load the Titanfall 2 `common.rpak` patch chain and export DTBL assets as CSV.
- [tf2vpk](https://github.com/pg9182/tf2vpk), MIT, source commit `b73c54d8e4245075ea207c7e51a2a86fdb94e4ff`, was used for read-only inspection of frontend VPK scripts.

The downloaded RSX 2.3.0 release archive matched the SHA-256 digest published by GitHub:

```text
589efc4ce8eb7185bfc936dce7def89e4b563404b3ee1112b60d60d26d3c2397
```

## Asset identity

RSX exported unnamed DTBL assets by GUID. To eliminate content-based guessing, the paths were hashed with a direct overflow-preserving port of RSX's `RTech::StringToGuid` implementation:

```text
datatable/xp_per_weapon_level.rpak -> 0x5FFC5DAB7723E105
datatable/pilot_weapons.rpak       -> 0xC75B1A213D67752C
```

The raw RSX export of `xp_per_weapon_level` had SHA-256:

```text
bb5a1c73e7e4221db34ff4bbb20bc672e57c2e5ee8b156dc179e61024a8f682d
```

It contained the five columns `level`, `default`, `sniper`, `pistol`, and `antititan`, followed by RSX's metadata type row (`int` for all columns). The public CSV omits that exporter-only metadata row and retains all 20 game-data rows unchanged.

## Weapon mappings

The original item initialization logic reads `itemRef` and `xpPerLevelType` from `datatable/pilot_weapons.rpak`, then calls `WeaponSetXPPerLevelType(itemRef, xpPerLevelType)`. The public mapping file contains the 12 weapons investigated in this dataset.

## Original progression logic

During initialization, the game builds two arrays per XP type:

```text
pips[level]       = the corresponding datatable row value
xpForLevel[1]     = 0
xpForLevel[level] = sum of rows before that internal level
```

The relevant original functions are equivalent to:

```text
maxXPPerGen = sum(rows 1..20)
generation  = floor(totalXP / maxXPPerGen) + 1
xpIntoGen   = totalXP % maxXPPerGen
level       = threshold lookup using a strict less-than comparison
```

The original display function shows the internal level unchanged in Generation 1, but displays `internal level - 1` from Generation 2 onward. Therefore an exact Generation boundary is `G2.0`, not `G2.1`.

For a displayed rank `Gg.s`, where `g > 1`:

```text
minimumXP = (g - 1) × maxXPPerGen + sum(rows 1..s)
```

## Validation

For every example row:

1. The weapon mapping was uniquely matched by `itemRef`.
2. The per-Generation total was recalculated from all 20 rows.
3. The minimum XP was passed through equivalent Generation and level functions.
4. The result displayed the requested rank.
5. Subtracting one XP displayed the preceding rank.

The 12 example minimum values sum to `15,414` weapon XP/pips. The current displayed ranks hide partial progress, so the sum of actual weapon XP can be between `15,414` and `15,491` for those examples.

## XP is not unconditionally equal to final kills

The progression logic reads a `weaponXP` field and separately reads a `proScreenKills` field. Northstar's score-event reconstruction awards one weapon XP for selected Pilot, Titan, and Auto-Titan kill/elimination events, and can multiply weapon XP under double-XP settings. Custom servers can also change progression behavior.

For those reasons, this repository reports weapon XP/pips. It does not relabel the values as a guaranteed count of human-player kills.

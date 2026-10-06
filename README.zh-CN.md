# 泰坦陨落 2 武器 XP / Generation 进度数据

[English README](README.md)

这是一个从本机正版安装文件中只读提取并核验的 **Titanfall 2 武器等级数据集**，包含：

- `xp_per_weapon_level.rpak` 的完整 20 级数值；
- 武器使用的 `xpPerLevelType`；
- 每个完整 Generation 所需的 Weapon XP/pips；
- 原版显示等级的差一规则；
- 一个不需要第三方库的自动计算器。

## 最重要的结论

原版并不存在“所有武器一代固定 200 杀”的统一规则：

| xpPerLevelType | 每个完整 Generation |
|---|---:|
| `default` | **185 XP/pips** |
| `sniper` | **94 XP/pips** |
| `pistol` | **94 XP/pips** |
| `antititan` | **77 XP/pips** |

这些单位是 Weapon XP/pips，不应无条件称为真人击杀数。双倍 XP、泰坦/自动泰坦消灭事件、自定义服务器规则，以及当前小等级中没有显示出来的进度，都可能让实际击杀数与 XP 不同。

## 完整原始等级表

已验证的资产路径是 `datatable/xp_per_weapon_level.rpak`，RTech GUID 为 `0x5FFC5DAB7723E105`。

| level | default | sniper | pistol | antititan |
|---:|---:|---:|---:|---:|
| 1 | 3 | 2 | 2 | 2 |
| 2 | 5 | 3 | 3 | 3 |
| 3 | 7 | 4 | 4 | 4 |
| 4 | 10 | 5 | 5 | 4 |
| 5 | 10 | 5 | 5 | 4 |
| 6 | 10 | 5 | 5 | 4 |
| 7 | 10 | 5 | 5 | 4 |
| 8 | 10 | 5 | 5 | 4 |
| 9 | 10 | 5 | 5 | 4 |
| 10 | 10 | 5 | 5 | 4 |
| 11 | 10 | 5 | 5 | 4 |
| 12 | 10 | 5 | 5 | 4 |
| 13 | 10 | 5 | 5 | 4 |
| 14 | 10 | 5 | 5 | 4 |
| 15 | 10 | 5 | 5 | 4 |
| 16 | 10 | 5 | 5 | 4 |
| 17 | 10 | 5 | 5 | 4 |
| 18 | 10 | 5 | 5 | 4 |
| 19 | 10 | 5 | 5 | 4 |
| 20 | 10 | 5 | 5 | 4 |

CSV 文件见 [`data/xp_per_weapon_level.csv`](data/xp_per_weapon_level.csv)。

## 正确的显示等级公式

原版在第 2 代以后显示的是“内部等级减 1”，所以刚完成第一代时显示 `G2.0`，而不是 `G2.1`。

对显示等级 `Gg.s`（`g > 1`）：

```text
最低累计 XP = (g - 1) × 每代总 XP + 第 1 至 s 行之和
```

例如 CAR `G25.2`：

```text
24 × 185 + 3 + 5 = 4,448 XP
```

## 计算器

只需要 Python 3：

```console
python tools/calculate_weapon_xp.py CAR G25.2
python tools/calculate_weapon_xp.py 小帮手精英 G3.6
python tools/calculate_weapon_xp.py 雷电球 38.8 --json
```

计算器同时给出：

- 每代所需 XP；
- 达到目标显示等级的最低累计 XP；
- 在不升到下一级的情况下，当前等级可能包含的 XP 区间。

## 数据来源与复核

- RPAK 提取工具：[RSX](https://github.com/r-ex/rsx) 2.3.0；
- VPK 只读检查工具：[tf2vpk](https://github.com/pg9182/tf2vpk)；
- `xp_per_weapon_level.rpak` GUID：`0x5FFC5DAB7723E105`；
- `pilot_weapons.rpak` GUID：`0xC75B1A213D67752C`；
- 计算结果按原版 `WeaponGetMaxXPPerGen`、`WeaponGetGenForXP`、`WeaponGetLevelForXP` 和显示函数逐项回算；
- 每个示例的最低值减 1 后都会回到前一个显示等级。

详细方法见 [`docs/methodology.md`](docs/methodology.md)。

## 版权和免责声明

本仓库不上传 RPAK/VPK、完整原版游戏脚本或解包器二进制文件。仓库中的原创说明和计算程序采用 MIT License；Titanfall、Titanfall 2、Respawn 及相关游戏资产归各自权利人所有。

这是非官方社区研究项目，与 EA、Respawn Entertainment 或 Northstar 项目没有隶属或背书关系。

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "calculate_weapon_xp.py"
SPEC = importlib.util.spec_from_file_location("calculate_weapon_xp", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class WeaponXPTests(unittest.TestCase):
    def test_requested_weapon_examples(self):
        expected = {
            ("CAR", "G25.2"): (4448, 4454),
            ("R-97", "G22.7"): (3940, 3949),
            ("Volt", "G2.15"): (320, 329),
            ("DMR", "G2.4"): (108, 112),
            ("EVA-8", "G2.10"): (270, 279),
            ("SMR", "G4.11"): (650, 659),
            ("EPG", "G3.15"): (505, 514),
            ("Wingman Elite", "G3.6"): (415, 424),
            ("RE-45", "G2.8"): (128, 132),
            ("Charge Rifle", "G13.11"): (965, 968),
            ("Thunderbolt", "G38.8"): (2878, 2881),
            ("Archer", "G11.5"): (787, 790),
        }
        for key, values in expected.items():
            with self.subTest(weapon=key[0], rank=key[1]):
                result = MODULE.calculate(*key)
                self.assertEqual(result.minimum_cumulative_weapon_xp, values[0])
                self.assertEqual(result.maximum_xp_before_next_displayed_rank, values[1])

    def test_generation_boundary_is_displayed_as_dot_zero(self):
        result = MODULE.calculate("CAR", "G2.0")
        self.assertEqual(result.minimum_cumulative_weapon_xp, 185)
        self.assertEqual(result.maximum_xp_before_next_displayed_rank, 187)

    def test_generation_one_uses_unshifted_display_level(self):
        first = MODULE.calculate("CAR", "G1.1")
        twentieth = MODULE.calculate("CAR", "1.20")
        self.assertEqual(first.minimum_cumulative_weapon_xp, 0)
        self.assertEqual(twentieth.minimum_cumulative_weapon_xp, 175)

    def test_chinese_alias(self):
        result = MODULE.calculate("雷电球", "38.8")
        self.assertEqual(result.weapon, "Thunderbolt")
        self.assertEqual(result.minimum_cumulative_weapon_xp, 2878)

    def test_invalid_generation_two_sublevel(self):
        with self.assertRaises(ValueError):
            MODULE.calculate("CAR", "G2.20")


if __name__ == "__main__":
    unittest.main()

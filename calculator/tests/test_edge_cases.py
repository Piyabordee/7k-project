"""
Edge Case and Boundary Value Tests

Tests boundary conditions, zero values, negative inputs,
overflow scenarios, and precision handling.
"""

import pytest
from decimal import Decimal, InvalidOperation, Overflow, DivisionByZero

from damage_calc import (
    to_decimal,
    calculate_total_atk,
    calculate_dmg_hp,
    calculate_cap_atk,
    calculate_final_dmg_hp,
    calculate_raw_dmg,
    calculate_effective_def,
    calculate_final_dmg,
)


# ============================================================================
# Zero Value Tests
# ============================================================================

class TestZeroValues:
    """Test behavior with zero inputs"""

    def test_zero_atk_char(self):
        """Zero ATK_CHAR with other non-zero values"""
        result = calculate_total_atk(
            Decimal("0"), Decimal("500"), Decimal("1500"),
            Decimal("50"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        # Should only have pet + base bonus
        assert result > Decimal("0")
        assert result < Decimal("3000")

    def test_zero_atk_pet(self):
        """Zero ATK_PET"""
        result = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("42"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert result > Decimal("5000")

    def test_zero_formation(self):
        """Zero formation bonus"""
        result = calculate_total_atk(
            Decimal("5000"), Decimal("400"), Decimal("1500"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert result == Decimal("5400")  # 5000 + 400

    def test_zero_skill_dmg(self):
        """Zero skill damage should return zero ATK-based damage"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("0"),
            crit_dmg=Decimal("288"),
            weak_dmg=Decimal("65"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
            final_dmg_hp=Decimal("0")
        )
        assert result == Decimal("0")

    def test_zero_crit_dmg(self):
        """Zero crit damage"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("100"),
            crit_dmg=Decimal("0"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        assert result == Decimal("0")

    def test_zero_def_target(self):
        """Zero DEF target"""
        result = calculate_effective_def(
            def_target=Decimal("0"),
            def_buff=Decimal("0"),
            def_reduce=Decimal("0"),
            ignore_def=Decimal("0")
        )
        assert result == Decimal("1")

    def test_all_zeros_total_atk(self):
        """All zeros in Total ATK calculation"""
        result = calculate_total_atk(
            Decimal("0"), Decimal("0"), Decimal("0"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert result == Decimal("0")

    def test_zero_hp_target(self):
        """Zero HP target for HP-based damage"""
        result = calculate_dmg_hp(
            hp_target=Decimal("0"),
            bonus_dmg_hp_target=Decimal("7")
        )
        assert result == Decimal("0")

    def test_zero_raw_damage(self):
        """Zero raw damage"""
        result = calculate_final_dmg(
            raw_dmg=Decimal("0"),
            effective_def=Decimal("2")
        )
        assert result == 0


# ============================================================================
# Boundary Value Tests
# ============================================================================

class TestBoundaryValues:
    """Test values at boundaries of valid ranges"""

    # Typical game value boundaries
    MAX_ATK = Decimal("10000")  # Max reasonable ATK
    MAX_HP = Decimal("100000000")  # 100M HP (boss)
    MAX_CRIT_DMG = Decimal("500")  # 500% crit damage
    MAX_DEF = Decimal("5000")  # Max reasonable DEF

    def test_minimum_positive_values(self):
        """Test with minimum positive (0.01) values"""
        result = calculate_total_atk(
            Decimal("0.01"), Decimal("0.01"), Decimal("0.01"),
            Decimal("0.01"), Decimal("0.01"), Decimal("0.01"), Decimal("0.01")
        )
        assert result > Decimal("0")
        assert result < Decimal("1")

    def test_max_atk_value(self):
        """Test with maximum ATK value"""
        result = calculate_total_atk(
            self.MAX_ATK, Decimal("0"), Decimal("1500"),
            Decimal("100"), Decimal("0"), Decimal("100"), Decimal("0")
        )
        # Should handle large values correctly
        assert result > self.MAX_ATK

    def test_max_hp_value(self):
        """Test with maximum HP value (boss)"""
        result = calculate_dmg_hp(
            hp_target=self.MAX_HP,
            bonus_dmg_hp_target=Decimal("7")
        )
        assert result == Decimal("7000000")

    def test_max_crit_dmg(self):
        """Test with maximum crit damage"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("100"),
            crit_dmg=self.MAX_CRIT_DMG,
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        # 5000 * 1.0 * 5.0 = 25000
        assert result == Decimal("25000")

    def test_max_def_value(self):
        """Test with maximum DEF value"""
        result = calculate_effective_def(
            def_target=self.MAX_DEF,
            def_buff=Decimal("100"),
            def_reduce=Decimal("0"),
            ignore_def=Decimal("0")
        )
        assert result > Decimal("1")

    def test_skill_dmg_boundary_100(self):
        """Test skill damage at 100% (common value)"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("100"),
            crit_dmg=Decimal("100"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        assert result == Decimal("5000")

    def test_skill_dmg_boundary_200(self):
        """Test skill damage at 200% (high value)"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("200"),
            crit_dmg=Decimal("100"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        assert result == Decimal("10000")

    def test_formation_boundaries(self):
        """Test formation at 0%, 50%, 100%"""
        atk_base = Decimal("1500")

        # 0% formation
        f0 = calculate_total_atk(
            Decimal("5000"), Decimal("0"), atk_base,
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")
        )

        # 50% formation
        f50 = calculate_total_atk(
            Decimal("5000"), Decimal("0"), atk_base,
            Decimal("50"), Decimal("0"), Decimal("0"), Decimal("0")
        )

        # 100% formation
        f100 = calculate_total_atk(
            Decimal("5000"), Decimal("0"), atk_base,
            Decimal("100"), Decimal("0"), Decimal("0"), Decimal("0")
        )

        assert f0 < f50 < f100
        assert f50 == Decimal("5750")  # 5000 + 750


# ============================================================================
# Precision and Rounding Tests
# ============================================================================

class TestPrecisionAndRounding:
    """Test Decimal precision and rounding behavior"""

    def test_decimal_precision(self):
        """Test Decimal precision is maintained"""
        result = calculate_total_atk(
            Decimal("5000.555"), Decimal("400.333"), Decimal("1500"),
            Decimal("42.5"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        # Should maintain precision
        assert isinstance(result, Decimal)

    def test_round_down_in_final_damage(self):
        """Test that final damage rounds down"""
        # 5001 / 2 = 2500.5 → 2500
        result = calculate_final_dmg(
            raw_dmg=Decimal("5001"),
            effective_def=Decimal("2")
        )
        assert result == 2500

    def test_round_down_at_point_nine(self):
        """Test 0.9 rounds down"""
        result = calculate_final_dmg(
            raw_dmg=Decimal("5000.9"),
            effective_def=Decimal("1")
        )
        assert result == 5000

    def test_round_down_hp_alteration(self):
        """Test HP alteration rounds down"""
        result = calculate_final_dmg_hp(
            dmg_hp=Decimal("1000.9"),
            cap_atk=Decimal("2000")
        )
        assert result == Decimal("1000")

    def test_fractional_percentages(self):
        """Test fractional percentage values"""
        result = calculate_dmg_hp(
            hp_target=Decimal("10000"),
            bonus_dmg_hp_target=Decimal("3.5")  # 3.5%
        )
        assert result == Decimal("350")


# ============================================================================
# Overflow and Large Value Tests
# ============================================================================

class TestOverflowAndLargeValues:
    """Test handling of very large values"""

    def test_very_large_atk(self):
        """Test with extremely large ATK value"""
        result = calculate_total_atk(
            Decimal("100000"), Decimal("0"), Decimal("1500"),
            Decimal("100"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        # Should handle without overflow
        assert result > Decimal("100000")

    def test_very_large_hp(self):
        """Test with 1 billion HP"""
        result = calculate_dmg_hp(
            hp_target=Decimal("1000000000"),  # 1B
            bonus_dmg_hp_target=Decimal("7")
        )
        assert result == Decimal("70000000")

    def test_large_skill_dmg(self):
        """Test with large skill damage percentage"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("500"),  # 500%
            crit_dmg=Decimal("100"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        assert result == Decimal("25000")

    def test_all_max_values_combined(self):
        """Test with all maximum values"""
        # This tests if system handles extreme scenarios
        result = calculate_raw_dmg(
            total_atk=Decimal("100000"),
            skill_dmg=Decimal("500"),
            crit_dmg=Decimal("500"),
            weak_dmg=Decimal("100"),
            dmg_amp_buff=Decimal("100"),
            dmg_amp_debuff=Decimal("50"),
            dmg_reduction=Decimal("0"),
        )
        # Should be astronomical but not overflow
        assert result > Decimal("0")


# ============================================================================
# Negative Value Tests
# ============================================================================

class TestNegativeValues:
    """Test handling of negative values"""

    def test_negative_atk_char(self):
        """Negative ATK_CHAR - Decimal handles it fine"""
        # In real game, negative ATK shouldn't happen
        # But Decimal accepts negative values
        result = calculate_total_atk(
            Decimal("-100"), Decimal("0"), Decimal("1500"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        # Result will be negative (from -100 + 1500 * 0%)
        assert result < Decimal("1500")

    def test_negative_skill_dmg(self):
        """Negative skill damage should produce negative or zero"""
        # This shouldn't happen in game, but tests robustness
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("-10"),  # Invalid in game
            crit_dmg=Decimal("100"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        # Negative skill damage would reduce damage
        assert result < Decimal("0")

    def test_negative_def_target(self):
        """Negative DEF target"""
        # Decimal handles negative DEF but result would be < 1
        result = calculate_effective_def(
            Decimal("-100"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        # Result would be less than 1 (negative DEF reduces defense)
        assert result < Decimal("1")


# ============================================================================
# Division and Edge Cases
# ============================================================================

class TestDivisionEdgeCases:
    """Test division-related edge cases"""

    def test_division_by_zero_prevention(self):
        """Test that division by zero is handled"""
        # calculate_effective_def multiplies by DEF_Modifier
        # If DEF_Target is 0, result is 1 (no division)
        result = calculate_effective_def(
            def_target=Decimal("0"),
            def_buff=Decimal("0"),
            def_reduce=Decimal("0"),
            ignore_def=Decimal("0")
        )
        assert result == Decimal("1")

    def test_fractional_results(self):
        """Test calculations that produce fractions"""
        # 5000 / 3 = 1666.666...
        result = calculate_final_dmg(
            raw_dmg=Decimal("5000"),
            effective_def=Decimal("3")
        )
        assert result == 1666  # Rounded down

    def test_very_small_effective_def(self):
        """Test with effective DEF close to 1"""
        result = calculate_final_dmg(
            raw_dmg=Decimal("5000"),
            effective_def=Decimal("1.0001")
        )
        # Should be close to raw damage
        assert 4999 <= result <= 5000


# ============================================================================
# Special Input Combinations
# ============================================================================

class TestSpecialCombinations:
    """Test unusual but valid input combinations"""

    def test_crit_dmg_100_no_multiplier(self):
        """Test crit damage of 100% (no bonus)"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("100"),
            crit_dmg=Decimal("100"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        # 5000 * 1.0 * 1.0 = 5000
        assert result == Decimal("5000")

    def test_weakness_base_30_only(self):
        """Test weakness with only base 30% (no bonus)"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("100"),
            crit_dmg=Decimal("288"),
            weak_dmg=Decimal("30"),  # Base only
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        # 5000 * 1.0 * 2.88 * 1.3
        expected = Decimal("18720")
        assert result == expected

    def test_dmg_amp_debuff_exceeds_reduction(self):
        """Test when DMG_AMP_DEBUFF > DMG_Reduction"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("100"),
            crit_dmg=Decimal("288"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("24"),
            dmg_reduction=Decimal("10"),  # Less than debuff
            final_dmg_hp=Decimal("0")
        )
        # Should increase damage
        no_debuff = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("100"),
            crit_dmg=Decimal("288"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("10"),
            final_dmg_hp=Decimal("0")
        )
        assert result > no_debuff

    def test_ignore_def_100_percent(self):
        """Test 100% Ignore_DEF (extreme case)"""
        result = calculate_effective_def(
            def_target=Decimal("1461"),
            def_buff=Decimal("0"),
            def_reduce=Decimal("0"),
            ignore_def=Decimal("100")
        )
        # Should be 1.0 (ignore all DEF)
        assert result == Decimal("1")


# ============================================================================
# Type Conversion Tests
# ============================================================================

class TestTypeConversion:
    """Test to_decimal with various input types"""

    def test_zero_integer(self):
        """Convert zero integer"""
        result = to_decimal(0)
        assert result == Decimal("0")

    def test_negative_integer(self):
        """Convert negative integer"""
        result = to_decimal(-100)
        assert result == Decimal("-100")

    def test_scientific_notation_string(self):
        """Convert scientific notation string"""
        result = to_decimal("1.5E+3")
        assert result == Decimal("1500")

    def test_very_long_decimal_string(self):
        """Convert long decimal string"""
        result = to_decimal("1234.567890123456789")
        assert result == Decimal("1234.567890123456789")

    def test_float_precision_issue(self):
        """Test float to Decimal conversion precision"""
        # 0.1 + 0.2 != 0.3 in float
        # But to_decimal uses str() to avoid this
        result = to_decimal(0.1)
        # Should be exactly 0.1, not approximation
        assert result == Decimal("0.1")


# ============================================================================
# Real Game Scenarios (Edge Cases)
# ============================================================================

class TestRealGameEdgeCases:
    """Test edge cases from actual game scenarios"""

    def test_castle_room_low_hp_monster(self):
        """Test castle monster with low HP"""
        hp_target = Decimal("8650")  # Castle Room 1
        result = calculate_dmg_hp(
            hp_target=hp_target,
            bonus_dmg_hp_target=Decimal("7")
        )
        assert result == Decimal("605.5")

    def test_transcended_character_stats(self):
        """Test transcended character (very high stats)"""
        result = calculate_total_atk(
            Decimal("8000"),  # Transcended ATK
            Decimal("500"),
            Decimal("1500"),
            Decimal("60"),  # High formation
            Decimal("10"),
            Decimal("30"),
            Decimal("10")
        )
        # Should handle transcended stats
        assert result > Decimal("10000")

    def test_minimal_stats_new_character(self):
        """Test new character with minimal stats"""
        result = calculate_total_atk(
            Decimal("100"),  # New character
            Decimal("0"),
            Decimal("1500"),
            Decimal("0"),  # No formation
            Decimal("0"),
            Decimal("0"),
            Decimal("0")
        )
        # 100 + 0 + (1500 * 0/100) = 100
        assert result == Decimal("100")

    def test_pvp_vs_pve_def_difference(self):
        """Test difference between PvP and PvE DEF"""
        pvp_def = calculate_effective_def(
            Decimal("2000"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        pve_def = calculate_effective_def(
            Decimal("800"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert pvp_def > pve_def


# ============================================================================
# Concurrent Modifier Tests
# ============================================================================

class TestConcurrentModifiers:
    """Test when multiple modifiers affect same stat"""

    def test_def_buff_and_reduce_together(self):
        """Test DEF_BUFF and DEF_REDUCE cancel out"""
        # 50% buff and 50% reduce should cancel
        result = calculate_effective_def(
            def_target=Decimal("1461"),
            def_buff=Decimal("50"),
            def_reduce=Decimal("50"),
            ignore_def=Decimal("0")
        )
        # Should be close to base DEF
        base = calculate_effective_def(
            Decimal("1461"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert abs(result - base) < Decimal("0.1")

    def test_dmg_amp_and_reduction_cancel(self):
        """Test DMG_AMP_DEBUFF and DMG_Reduction interaction"""
        equal = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("0"), Decimal("0"), Decimal("10"), Decimal("10")
        )
        only_reduction = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("10")
        )
        # Should be higher with debuff cancelling reduction
        assert equal > only_reduction

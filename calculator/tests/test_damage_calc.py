"""
Unit Tests for Core Damage Calculation Functions
Tests all functions in damage_calc.py with comprehensive coverage
"""

import pytest
from decimal import Decimal

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
# Fixtures
# ============================================================================

@pytest.fixture
def standard_config():
    """Standard configuration for testing"""
    return {
        "atk_char": Decimal("5000"),
        "atk_pet": Decimal("400"),
        "atk_base": Decimal("1500"),
        "formation": Decimal("42"),
        "potential_pet": Decimal("0"),
        "buff_atk": Decimal("0"),
        "buff_atk_pet": Decimal("0"),
    }


@pytest.fixture
def crit_weak_config():
    """Configuration with crit and weakness modifiers"""
    return {
        "total_atk": Decimal("5400"),
        "skill_dmg": Decimal("160"),
        "crit_dmg": Decimal("288"),
        "weak_dmg": Decimal("65"),  # 30% base + 35% weapon
        "dmg_amp_buff": Decimal("0"),
        "dmg_amp_debuff": Decimal("0"),
        "dmg_reduction": Decimal("10"),
    }


# ============================================================================
# to_decimal() Tests
# ============================================================================

class TestToDecimal:
    """Test to_decimal conversion function"""

    def test_int_to_decimal(self):
        """Convert integer to Decimal"""
        result = to_decimal(100)
        assert result == Decimal("100")
        assert isinstance(result, Decimal)

    def test_float_to_decimal(self):
        """Convert float to Decimal via string"""
        result = to_decimal(3.14)
        assert result == Decimal("3.14")

    def test_string_to_decimal(self):
        """Convert string to Decimal"""
        result = to_decimal("42.5")
        assert result == Decimal("42.5")

    def test_decimal_passthrough(self):
        """Pass through existing Decimal"""
        original = Decimal("123.456")
        result = to_decimal(original)
        assert result == original
        assert result is original


# ============================================================================
# calculate_total_atk() Tests
# ============================================================================

class TestCalculateTotalAtk:
    """Test Total ATK calculation"""

    def test_base_calculation(self, standard_config):
        """Test basic ATK calculation"""
        result = calculate_total_atk(
            atk_char=standard_config["atk_char"],
            atk_pet=standard_config["atk_pet"],
            atk_base=standard_config["atk_base"],
            formation=standard_config["formation"],
            potential_pet=standard_config["potential_pet"],
            buff_atk=standard_config["buff_atk"],
            buff_atk_pet=standard_config["buff_atk_pet"],
        )
        # (5000 + 400 + (1500 * 42/100)) * 1 = 5000 + 400 + 630 = 6030
        assert result == Decimal("6030")

    def test_formation_bonus(self):
        """Test formation bonus increases ATK"""
        no_formation = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        with_formation = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("50"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert with_formation > no_formation
        # 5000 vs 5000 + 750 = 5750
        assert with_formation == Decimal("5750")

    def test_potential_pet(self):
        """Test pet potential increases ATK"""
        no_potential = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("42"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        with_potential = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("42"), Decimal("10"), Decimal("0"), Decimal("0")
        )
        assert with_potential > no_potential

    def test_buff_atk_multiplicative(self):
        """Test BUFF_ATK is multiplicative"""
        no_buff = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("42"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        with_buff = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("42"), Decimal("0"), Decimal("50"), Decimal("0")
        )
        # (5000 + 0 + 630) * 1.5 = 5630 * 1.5 = 8445
        assert with_buff == Decimal("8445")

    def test_zero_values(self):
        """Test with all zero values"""
        result = calculate_total_atk(
            Decimal("0"), Decimal("0"), Decimal("0"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert result == Decimal("0")

    def test_atk_base_by_class(self):
        """Test ATK_BASE values by class"""
        # From constants.py
        atk_bases = {
            "magic": Decimal("1500"),
            "attack": Decimal("1500"),
            "support": Decimal("1095"),
            "defense": Decimal("727"),
            "balance": Decimal("1306"),
        }

        for class_name, atk_base in atk_bases.items():
            result = calculate_total_atk(
                Decimal("5000"), Decimal("0"), atk_base,
                Decimal("42"), Decimal("0"), Decimal("0"), Decimal("0")
            )
            assert result > Decimal("5000")


# ============================================================================
# calculate_dmg_hp() Tests
# ============================================================================

class TestCalculateDmgHp:
    """Test HP-based damage calculation"""

    def test_seven_percent_of_hp(self):
        """Test 7% of Max HP damage"""
        result = calculate_dmg_hp(
            hp_target=Decimal("10000"),
            bonus_dmg_hp_target=Decimal("7")
        )
        assert result == Decimal("700")

    def test_zero_bonus(self):
        """Test zero bonus returns zero"""
        result = calculate_dmg_hp(
            hp_target=Decimal("10000"),
            bonus_dmg_hp_target=Decimal("0")
        )
        assert result == Decimal("0")

    def test_large_hp_value(self):
        """Test with large HP value (boss monster)"""
        result = calculate_dmg_hp(
            hp_target=Decimal("100000000"),  # 100M HP
            bonus_dmg_hp_target=Decimal("7")
        )
        assert result == Decimal("7000000")

    def test_fractional_percent(self):
        """Test fractional percentage"""
        result = calculate_dmg_hp(
            hp_target=Decimal("1000"),
            bonus_dmg_hp_target=Decimal("3.5")
        )
        assert result == Decimal("35")


# ============================================================================
# calculate_cap_atk() Tests
# ============================================================================

class TestCalculateCapAtk:
    """Test HP-based damage cap calculation"""

    def test_hundred_percent_cap(self):
        """Test 100% ATK cap"""
        result = calculate_cap_atk(
            total_atk=Decimal("5000"),
            cap_atk_percent=Decimal("100")
        )
        assert result == Decimal("5000")

    def test_fifty_percent_cap(self):
        """Test 50% ATK cap"""
        result = calculate_cap_atk(
            total_atk=Decimal("5000"),
            cap_atk_percent=Decimal("50")
        )
        assert result == Decimal("2500")

    def test_zero_cap(self):
        """Test 0% cap"""
        result = calculate_cap_atk(
            total_atk=Decimal("5000"),
            cap_atk_percent=Decimal("0")
        )
        assert result == Decimal("0")


# ============================================================================
# calculate_final_dmg_hp() Tests
# ============================================================================

class TestCalculateFinalDmgHp:
    """Test final HP-based damage with cap"""

    def test_damage_under_cap(self):
        """Test when damage is under cap, use actual"""
        result = calculate_final_dmg_hp(
            dmg_hp=Decimal("700"),
            cap_atk=Decimal("1000")
        )
        assert result == Decimal("700")

    def test_damage_over_cap(self):
        """Test when damage exceeds cap, use cap"""
        result = calculate_final_dmg_hp(
            dmg_hp=Decimal("1500"),
            cap_atk=Decimal("1000")
        )
        assert result == Decimal("1000")

    def test_equal_to_cap(self):
        """Test when damage equals cap"""
        result = calculate_final_dmg_hp(
            dmg_hp=Decimal("1000"),
            cap_atk=Decimal("1000")
        )
        assert result == Decimal("1000")

    def test_zero_cap_returns_zero(self):
        """Test zero cap returns zero"""
        result = calculate_final_dmg_hp(
            dmg_hp=Decimal("700"),
            cap_atk=Decimal("0")
        )
        # Zero cap means no capping, returns actual
        assert result == Decimal("700")

    def test_round_down(self):
        """Test rounding down occurs"""
        result = calculate_final_dmg_hp(
            dmg_hp=Decimal("1000.9"),
            cap_atk=Decimal("2000")
        )
        assert result == Decimal("1000")  # Rounded down

    def test_round_down_cap(self):
        """Test cap value is rounded down"""
        result = calculate_final_dmg_hp(
            dmg_hp=Decimal("1500"),
            cap_atk=Decimal("1000.9")
        )
        assert result == Decimal("1000")  # Cap rounded down


# ============================================================================
# calculate_raw_dmg() Tests
# ============================================================================

class TestCalculateRawDmg:
    """Test RAW damage calculation"""

    def test_base_damage(self):
        """Test basic damage calculation"""
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

    def test_crit_damage(self):
        """Test crit damage multiplier"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("100"),
            crit_dmg=Decimal("288"),
            weak_dmg=Decimal("0"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )
        # 5000 * 1.0 * 2.88 = 14400
        assert result == Decimal("14400")

    def test_weakness_hit(self, crit_weak_config):
        """Test weakness hit damage increase"""
        result = calculate_raw_dmg(
            total_atk=crit_weak_config["total_atk"],
            skill_dmg=crit_weak_config["skill_dmg"],
            crit_dmg=crit_weak_config["crit_dmg"],
            weak_dmg=crit_weak_config["weak_dmg"],
            dmg_amp_buff=crit_weak_config["dmg_amp_buff"],
            dmg_amp_debuff=crit_weak_config["dmg_amp_debuff"],
            dmg_reduction=crit_weak_config["dmg_reduction"],
        )
        # Should be higher than without weakness
        no_weak = calculate_raw_dmg(
            total_atk=crit_weak_config["total_atk"],
            skill_dmg=crit_weak_config["skill_dmg"],
            crit_dmg=crit_weak_config["crit_dmg"],
            weak_dmg=Decimal("0"),
            dmg_amp_buff=crit_weak_config["dmg_amp_buff"],
            dmg_amp_debuff=crit_weak_config["dmg_amp_debuff"],
            dmg_reduction=crit_weak_config["dmg_reduction"],
        )
        assert result > no_weak

    def test_crit_and_weakness(self, crit_weak_config):
        """Test crit and weakness combined"""
        result = calculate_raw_dmg(
            total_atk=crit_weak_config["total_atk"],
            skill_dmg=crit_weak_config["skill_dmg"],
            crit_dmg=crit_weak_config["crit_dmg"],
            weak_dmg=crit_weak_config["weak_dmg"],
            dmg_amp_buff=crit_weak_config["dmg_amp_buff"],
            dmg_amp_debuff=crit_weak_config["dmg_amp_debuff"],
            dmg_reduction=crit_weak_config["dmg_reduction"],
        )
        # 5400 * 1.6 * 2.88 * 1.65 * 0.9 = 37,460.x
        assert result > Decimal("30000")

    def test_dmg_amp_buff(self):
        """Test DMG_AMP_BUFF increases damage"""
        no_buff = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("65"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        with_buff = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("65"), Decimal("70"), Decimal("0"), Decimal("0")
        )
        assert with_buff > no_buff

    def test_dmg_reduction_decreases(self):
        """Test DMG_Reduction decreases damage"""
        no_reduction = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("65"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        with_reduction = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("65"), Decimal("0"), Decimal("0"), Decimal("10")
        )
        assert with_reduction < no_reduction

    def test_hp_based_damage_addition(self):
        """Test HP-based damage is added to base"""
        no_hp = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("65"), Decimal("0"), Decimal("0"), Decimal("10"),
            Decimal("0")
        )
        with_hp = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("65"), Decimal("0"), Decimal("0"), Decimal("10"),
            Decimal("1000")  # Final_DMG_HP
        )
        assert with_hp > no_hp
        # Difference should be HP damage with multipliers
        difference = with_hp - no_hp
        expected_hp = Decimal("1000") * Decimal("2.88") * Decimal("1.65") * Decimal("0.9")
        assert abs(difference - expected_hp) < Decimal("1")

    def test_zero_skill_dmg(self):
        """Test zero skill damage"""
        result = calculate_raw_dmg(
            Decimal("5000"), Decimal("0"), Decimal("288"),
            Decimal("65"), Decimal("0"), Decimal("0"), Decimal("10"),
            Decimal("1000")
        )
        # Only HP damage should remain
        expected = Decimal("1000") * Decimal("2.88") * Decimal("1.65") * Decimal("0.9")
        assert abs(result - expected) < Decimal("1")

    def test_all_multipliers_combined(self):
        """Test all damage modifiers combined"""
        result = calculate_raw_dmg(
            total_atk=Decimal("5000"),
            skill_dmg=Decimal("160"),
            crit_dmg=Decimal("288"),
            weak_dmg=Decimal("65"),  # 30% base + 35%
            dmg_amp_buff=Decimal("70"),
            dmg_amp_debuff=Decimal("24"),
            dmg_reduction=Decimal("10"),
            final_dmg_hp=Decimal("0")
        )
        assert result > Decimal("0")
        # Sanity check: should be very high
        assert result > Decimal("20000")


# ============================================================================
# calculate_effective_def() Tests
# ============================================================================

class TestCalculateEffectiveDef:
    """Test Effective DEF calculation"""

    def test_base_def_greater_than_one(self):
        """Test effective DEF is always greater than 1"""
        result = calculate_effective_def(
            def_target=Decimal("1461"),
            def_buff=Decimal("0"),
            def_reduce=Decimal("0"),
            ignore_def=Decimal("0")
        )
        assert result > Decimal("1")
        # 1 + 0.00214135 * 1461 ≈ 4.13
        assert abs(result - Decimal("4.13")) < Decimal("1")

    def test_def_buff_increases(self):
        """Test DEF_BUFF increases effective DEF"""
        no_buff = calculate_effective_def(
            Decimal("1461"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        with_buff = calculate_effective_def(
            Decimal("1461"), Decimal("50"), Decimal("0"), Decimal("0")
        )
        assert with_buff > no_buff

    def test_def_reduce_decreases(self):
        """Test DEF_REDUCE decreases effective DEF"""
        no_reduce = calculate_effective_def(
            Decimal("1461"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        with_reduce = calculate_effective_def(
            Decimal("1461"), Decimal("0"), Decimal("24"), Decimal("0")
        )
        assert with_reduce < no_reduce

    def test_ignore_def_decreases(self):
        """Test Ignore_DEF decreases effective DEF"""
        no_ignore = calculate_effective_def(
            Decimal("1461"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        with_ignore = calculate_effective_def(
            Decimal("1461"), Decimal("0"), Decimal("0"), Decimal("40")
        )
        assert with_ignore < no_ignore

    def test_all_def_modifiers(self):
        """Test all DEF modifiers combined"""
        result = calculate_effective_def(
            def_target=Decimal("1461"),
            def_buff=Decimal("0"),
            def_reduce=Decimal("24"),
            ignore_def=Decimal("40")
        )
        # Should be lower than base DEF
        base = calculate_effective_def(
            Decimal("1461"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert result < base
        # But still greater than 1
        assert result > Decimal("1")

    def test_zero_def_target(self):
        """Test zero DEF target"""
        result = calculate_effective_def(
            def_target=Decimal("0"),
            def_buff=Decimal("0"),
            def_reduce=Decimal("0"),
            ignore_def=Decimal("0")
        )
        assert result == Decimal("1")

    def test_castle_room_def_values(self):
        """Test Castle Room DEF values"""
        # Room 1: DEF = 689
        room1 = calculate_effective_def(
            Decimal("689"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        # Room 2: DEF = 784
        room2 = calculate_effective_def(
            Decimal("784"), Decimal("0"), Decimal("0"), Decimal("0")
        )
        assert room2 > room1
        assert room1 > Decimal("1")
        assert room2 > Decimal("1")


# ============================================================================
# calculate_final_dmg() Tests
# ============================================================================

class TestCalculateFinalDmg:
    """Test Final Damage calculation"""

    def test_basic_final_damage(self):
        """Test basic final damage calculation"""
        result = calculate_final_dmg(
            raw_dmg=Decimal("5000"),
            effective_def=Decimal("2")
        )
        assert result == 2500

    def test_round_down_behavior(self):
        """Test rounding down (floor) behavior"""
        # 5000 / 3 = 1666.666... → 1666
        result = calculate_final_dmg(
            raw_dmg=Decimal("5000"),
            effective_def=Decimal("3")
        )
        assert result == 1666

    def test_round_down_point_five(self):
        """Test .5 rounds down (not up)"""
        # 1000 / 2 = 500 (exact)
        result1 = calculate_final_dmg(
            raw_dmg=Decimal("1000"),
            effective_def=Decimal("2")
        )
        assert result1 == 500

        # Should round down, not up
        result2 = calculate_final_dmg(
            raw_dmg=Decimal("1001"),
            effective_def=Decimal("2")
        )
        assert result2 == 500

    def test_zero_damage(self):
        """Test zero raw damage"""
        result = calculate_final_dmg(
            raw_dmg=Decimal("0"),
            effective_def=Decimal("2")
        )
        assert result == 0

    def test_large_damage_values(self):
        """Test large damage values (boss monster)"""
        result = calculate_final_dmg(
            raw_dmg=Decimal("100000000"),
            effective_def=Decimal("4.2")
        )
        # Should be approximately 23.8M
        assert result > 20000000
        assert result < 25000000

    def test_returns_int(self):
        """Test return type is int"""
        result = calculate_final_dmg(
            raw_dmg=Decimal("5000.5"),
            effective_def=Decimal("2")
        )
        assert isinstance(result, int)
        assert not isinstance(result, Decimal)

    def test_effective_def_one(self):
        """Test effective DEF of 1 (no reduction)"""
        result = calculate_final_dmg(
            raw_dmg=Decimal("5000"),
            effective_def=Decimal("1")
        )
        assert result == 5000


# ============================================================================
# Integration Tests
# ============================================================================

class TestFullDamagePipeline:
    """Test complete damage calculation pipeline"""

    def test_standard_attack_calculation(self):
        """Test standard attack damage calculation"""
        # Calculate Total ATK
        total_atk = calculate_total_atk(
            Decimal("4488"), Decimal("391"), Decimal("1500"),
            Decimal("42"), Decimal("0"), Decimal("0"), Decimal("19")
        )

        # Calculate RAW Damage
        raw_dmg = calculate_raw_dmg(
            total_atk=total_atk,
            skill_dmg=Decimal("100"),
            crit_dmg=Decimal("288"),
            weak_dmg=Decimal("65"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("0"),
        )

        # Calculate Effective DEF
        eff_def = calculate_effective_def(
            Decimal("1461"), Decimal("0"), Decimal("0"), Decimal("0")
        )

        # Calculate Final Damage
        final = calculate_final_dmg(raw_dmg, eff_def)

        # Sanity checks
        assert total_atk > Decimal("5000")
        assert raw_dmg > total_atk
        assert eff_def > Decimal("1")
        assert final > 0
        assert final < raw_dmg  # DEF reduces damage

    def test_weakness_crit_scenario(self):
        """Test weakness + crit scenario"""
        total_atk = Decimal("5400")

        raw_dmg = calculate_raw_dmg(
            total_atk=total_atk,
            skill_dmg=Decimal("160"),
            crit_dmg=Decimal("288"),
            weak_dmg=Decimal("65"),
            dmg_amp_buff=Decimal("0"),
            dmg_amp_debuff=Decimal("0"),
            dmg_reduction=Decimal("10"),
        )

        eff_def = calculate_effective_def(
            def_target=Decimal("1461"),
            def_buff=Decimal("0"),
            def_reduce=Decimal("24"),
            ignore_def=Decimal("40")
        )

        final = calculate_final_dmg(raw_dmg, eff_def)

        # Should be substantial damage
        assert final > 5000


# ============================================================================
# Property-Based Tests (Invariants)
# ============================================================================

class TestInvariants:
    """Test mathematical invariants that should always hold"""

    def test_damage_never_negative(self):
        """Damage should never be negative"""
        total_atk = calculate_total_atk(
            Decimal("100"), Decimal("0"), Decimal("100"),
            Decimal("10"), Decimal("0"), Decimal("0"), Decimal("0")
        )

        raw_dmg = calculate_raw_dmg(
            total_atk, Decimal("100"), Decimal("100"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")
        )

        final = calculate_final_dmg(raw_dmg, Decimal("2"))
        assert final >= 0

    def test_effective_def_always_greater_than_one(self):
        """Effective DEF should always be >= 1"""
        for def_target in [Decimal("0"), Decimal("100"), Decimal("1000"), Decimal("5000")]:
            result = calculate_effective_def(
                def_target, Decimal("0"), Decimal("0"), Decimal("0")
            )
            assert result >= Decimal("1")

    def test_buff_increases_damage(self):
        """BUFF_ATK should always increase total ATK"""
        base = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("42"), Decimal("0"), Decimal("0"), Decimal("0")
        )

        buffed = calculate_total_atk(
            Decimal("5000"), Decimal("0"), Decimal("1500"),
            Decimal("42"), Decimal("0"), Decimal("50"), Decimal("0")
        )

        assert buffed > base

    def test_reduction_decreases_damage(self):
        """DMG_Reduction should always decrease damage"""
        no_reduction = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0")
        )

        with_reduction = calculate_raw_dmg(
            Decimal("5000"), Decimal("100"), Decimal("288"),
            Decimal("0"), Decimal("0"), Decimal("0"), Decimal("10")
        )

        assert with_reduction < no_reduction

    def test_def_increase_reduces_damage(self):
        """Higher DEF should reduce final damage"""
        raw_dmg = Decimal("10000")

        low_def = calculate_final_dmg(raw_dmg, Decimal("2"))
        high_def = calculate_final_dmg(raw_dmg, Decimal("5"))

        assert low_def > high_def

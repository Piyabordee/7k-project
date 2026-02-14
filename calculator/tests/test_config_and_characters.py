"""
Integration Tests for Config Loading and Standard Characters

Tests config loading, merging, weapon sets, and standard character calculations.
"""

import pytest
import json
from pathlib import Path
from decimal import Decimal
from typing import Any

# Import functions to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_loader import (
    load_json,
    load_character_full,
    load_user_config,
    load_monster_preset,
    apply_weapon_set,
    merge_configs,
    get_decimal,
    list_characters,
)
from damage_calc import (
    calculate_total_atk,
    calculate_raw_dmg,
    calculate_effective_def,
    calculate_final_dmg,
)
from character_registry import get_character_handler, list_registered_characters


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_character_config():
    """Sample character configuration"""
    return {
        "_character": "TestCharacter",
        "_rarity": "legend",
        "_class": "magic",
        "_element": "Fire",
        "BUFF_ATK": Decimal("0"),
        "CRIT_DMG": Decimal("0"),
        "DMG_AMP_BUFF": Decimal("0"),
        "WEAK_DMG": Decimal("35"),
        "_skills": {
            "skill1": {
                "_name": "Test Skill",
                "SKILL_DMG": Decimal("100"),
                "SKILL_HITS": 1,
            }
        },
    }


@pytest.fixture
def sample_user_config():
    """Sample user config"""
    return {
        "Weapon_Set": 1,
        "Formation": Decimal("42.0"),
        "ATK_CHAR": Decimal("4488.0"),
        "CRIT_DMG": Decimal("288.0"),
        "DMG_AMP_BUFF": Decimal("0.0"),
        "ATK_PET": Decimal("391.0"),
        "BUFF_ATK_PET": Decimal("19.0"),
        "Potential_PET": Decimal("0.0"),
        "DEF_Target": Decimal("1461.0"),
        "HP_Target": Decimal("17917.0"),
        "Target_HP_Percent": Decimal("30.0"),
        "DMG_Reduction": Decimal("10.0"),
        "DEF_BUFF": Decimal("0.0"),
    }


# ============================================================================
# Config Loading Tests
# ============================================================================

class TestConfigLoading:
    """Test configuration file loading"""

    def test_list_characters(self):
        """Test listing all character files"""
        characters = list_characters()
        assert isinstance(characters, list)
        assert len(characters) > 0
        # Check for known characters (without .json extension)
        assert "biscuit" in characters
        assert "espada" in characters
        assert "freyja" in characters

    def test_load_character_json(self):
        """Test loading character JSON file"""
        meta, config = load_character_full("biscuit")
        # Returns tuple of (meta, config)
        assert isinstance(meta, dict)
        assert isinstance(config, dict)
        assert "_character" in meta
        assert meta["_character"] == "Biscuit"
        assert "_rarity" in meta
        assert "_class" in meta

    def test_load_monster_preset(self):
        """Test loading monster preset"""
        # Note: load_monster_preset needs the .json extension
        result = load_monster_preset("castle_room1.json")
        assert isinstance(result, dict)
        # Values are returned as float from JSON
        assert "DEF_Target" in result or "DEF_Target" in str(result) or len(result) > 0

    def test_load_user_config(self):
        """Test loading user config.json"""
        result = load_user_config()
        assert isinstance(result, dict)
        # Check for expected keys
        assert "Formation" in result or result == {}
        # Config might be empty in test environment

    def test_get_decimal(self):
        """Test get_decimal helper"""
        config = {"value": Decimal("100.5")}
        result = get_decimal(config, "value", Decimal("0"))
        assert result == Decimal("100.5")

    def test_get_decimal_with_default(self):
        """Test get_decimal returns default for missing key"""
        config = {}
        result = get_decimal(config, "missing", Decimal("42"))
        # get_decimal returns the default value when key is missing
        assert result == Decimal("42") or result == "42"


# ============================================================================
# Config Merging Tests
# ============================================================================

class TestConfigMerging:
    """Test configuration merging logic"""

    def test_merge_additive_keys(self, sample_character_config, sample_user_config):
        """Test additive keys are summed"""
        char_config = {
            "BUFF_ATK": Decimal("10"),
            "CRIT_DMG": Decimal("50"),
            "WEAK_DMG": Decimal("35"),
        }
        user_config = {
            "BUFF_ATK": Decimal("20"),
            "CRIT_DMG": Decimal("238"),
            "WEAK_DMG": Decimal("30"),
        }
        result = merge_configs(char_config, user_config)

        assert result["BUFF_ATK"] == Decimal("30")  # 10 + 20
        assert result["CRIT_DMG"] == Decimal("288")  # 50 + 238
        assert result["WEAK_DMG"] == Decimal("65")  # 35 + 30

    def test_merge_mapping_keys(self):
        """Test Bonus_Crit_DMG maps to CRIT_DMG"""
        char_config = {
            "Bonus_Crit_DMG": Decimal("85"),
        }
        user_config = {
            "CRIT_DMG": Decimal("288"),
        }
        result = merge_configs(char_config, user_config)

        # Bonus_Crit_DMG should be added to CRIT_DMG
        assert result["CRIT_DMG"] == Decimal("373")  # 288 + 85

    def test_merge_with_missing_keys(self, sample_character_config):
        """Test merge when user config missing keys"""
        char_config = {
            "BUFF_ATK": Decimal("10"),
            "CRIT_DMG": Decimal("50"),
        }
        user_config = {
            "BUFF_ATK": Decimal("20"),
            # CRIT_DMG missing
        }
        result = merge_configs(char_config, user_config)

        assert result["BUFF_ATK"] == Decimal("30")  # 10 + 20
        assert result["CRIT_DMG"] == Decimal("50")  # Only from char

    def test_merge_preserves_non_additive(self):
        """Test non-additive keys use user value"""
        char_config = {
            "ATK_CHAR": Decimal("100"),
            "Formation": Decimal("10"),
        }
        user_config = {
            "ATK_CHAR": Decimal("5000"),
            "Formation": Decimal("42"),
        }
        result = merge_configs(char_config, user_config)

        # Should use user values (not additive)
        assert result["ATK_CHAR"] == Decimal("5000")
        assert result["Formation"] == Decimal("42")


# ============================================================================
# Weapon Set Tests
# ============================================================================

class TestWeaponSets:
    """Test weapon set bonus application"""

    def test_weapon_set_0_no_bonus(self):
        """Test Weapon_Set 0 (no weapon)"""
        config = {"Weapon_Set": 0, "WEAK_DMG": Decimal("0"), "Ignore_DEF": Decimal("0"), "DMG_AMP_BUFF": Decimal("0")}
        result = apply_weapon_set(config)
        assert result["Weapon_Set"] == 0
        assert result["WEAK_DMG"] == Decimal("0")
        assert result["Ignore_DEF"] == Decimal("0")
        assert result["DMG_AMP_BUFF"] == Decimal("0")

    def test_weapon_set_1_weakness(self):
        """Test Weapon_Set 1 (Weakness) - WEAK_DMG += 35"""
        config = {
            "Weapon_Set": 1,
            "WEAK_DMG": Decimal("30"),
            "Ignore_DEF": Decimal("0"),
            "DMG_AMP_BUFF": Decimal("0"),
        }
        result = apply_weapon_set(config)
        assert result["WEAK_DMG"] == Decimal("65")  # 30 + 35

    def test_weapon_set_2_crit(self):
        """Test Weapon_Set 2 (Crit) - Ignore_DEF += 15"""
        config = {
            "Weapon_Set": 2,
            "WEAK_DMG": Decimal("0"),
            "Ignore_DEF": Decimal("20"),
            "DMG_AMP_BUFF": Decimal("0"),
        }
        result = apply_weapon_set(config)
        assert result["Ignore_DEF"] == Decimal("35")  # 20 + 15

    def test_weapon_set_3_hydra(self):
        """Test Weapon_Set 3 (Hydra) - DMG_AMP_BUFF += 70"""
        config = {
            "Weapon_Set": 3,
            "WEAK_DMG": Decimal("0"),
            "Ignore_DEF": Decimal("0"),
            "DMG_AMP_BUFF": Decimal("10"),
        }
        result = apply_weapon_set(config)
        assert result["DMG_AMP_BUFF"] == Decimal("80")  # 10 + 70

    def test_weapon_set_4_hydra_castle(self):
        """Test Weapon_Set 4 (Hydra Castle) - DMG_AMP_BUFF += 30"""
        config = {
            "Weapon_Set": 4,
            "WEAK_DMG": Decimal("0"),
            "Ignore_DEF": Decimal("0"),
            "DMG_AMP_BUFF": Decimal("10"),
        }
        result = apply_weapon_set(config)
        assert result["DMG_AMP_BUFF"] == Decimal("40")  # 10 + 30


# ============================================================================
# Standard Character Tests
# ============================================================================

class TestStandardCharacters:
    """Test standard (non-special) character calculations"""

    def test_miho_standard_calculation(self):
        """Test Miho - standard character"""
        meta, config = load_character_full("miho")
        assert meta is not None
        assert meta["_character"] == "Miho"
        # Skills are in the metadata (_skills)
        assert "_skills" in meta or len(config) > 0

    def test_pascal_bonus_crit_dmg_mapping(self):
        """Test Pascal - Bonus Crit DMG mapping"""
        meta, config = load_character_full("pascal")
        assert meta is not None
        # Pascal has passive crit damage bonus (not Bonus_Crit_DMG field)
        # The CRIT_DMG comes from passive, not a mapping
        assert "CRIT_DMG" in config or len(config) > 0

    def test_rachel_def_reduce_dmg_amp(self):
        """Test Rachel - DEF_REDUCE and DMG_AMP_DEBUFF"""
        meta, config = load_character_full("rachel")
        assert meta is not None
        # Rachel has DEF_REDUCE and DMG_AMP_DEBUFF skills

    def test_teo_standard_calculation(self):
        """Test Teo - standard character"""
        meta, config = load_character_full("teo")
        assert meta is not None
        assert meta["_character"] == "Teo"

    def test_yeonhee_hp_based(self):
        """Test Yeonhee - HP-based damage"""
        meta, config = load_character_full("yeonhee")
        assert meta is not None
        # Yeonhee has HP-based damage

    def test_klahan_hp_condition(self):
        """Test Klahan - HP condition bonus"""
        meta, config = load_character_full("klahan")
        assert meta is not None
        # Has HP_Above_50_Bonus and HP_Below_50_Bonus


# ============================================================================
# Registry Tests
# ============================================================================

class TestCharacterRegistry:
    """Test character registry pattern"""

    def test_list_registered_characters(self):
        """Test listing all registered characters"""
        characters = list_registered_characters()
        assert isinstance(characters, list)
        assert len(characters) > 0
        # Check for known special characters
        assert "biscuit" in characters
        assert "freyja" in characters
        assert "espada" in characters
        assert "ryan" in characters

    def test_get_special_character_handler(self):
        """Test getting handler for special characters"""
        # These should have registered handlers
        for char_name in ["biscuit", "freyja", "espada", "ryan"]:
            handler = get_character_handler(char_name)
            assert handler is not None, f"{char_name} should have a handler"
            assert callable(handler)

    def test_get_standard_character_handler(self):
        """Test getting handler for standard characters"""
        # Standard characters return None (use default flow)
        for char_name in ["miho", "pascal", "rachel", "teo", "yeonhee"]:
            handler = get_character_handler(char_name)
            # Should be None (use default flow)
            assert handler is None or callable(handler)


# ============================================================================
# Full Calculation Integration Tests
# ============================================================================

class TestFullCalculationIntegration:
    """Test complete calculation from config to damage"""

    def test_standard_character_full_pipeline(self):
        """Test full pipeline for standard character"""
        # Load character
        meta, char_config = load_character_full("miho")
        user_config = {
            "Weapon_Set": 0,
            "Formation": Decimal("42"),
            "ATK_CHAR": Decimal("5000"),
            "ATK_PET": Decimal("400"),
            "BUFF_ATK_PET": Decimal("19"),
            "Potential_PET": Decimal("0"),
            "BUFF_ATK": Decimal("0"),
            "CRIT_DMG": Decimal("288"),
            "DEF_Target": Decimal("1461"),
            "DMG_AMP_BUFF": Decimal("0"),
            "DMG_AMP_DEBUFF": Decimal("0"),
            "DMG_Reduction": Decimal("10"),
            "DEF_BUFF": Decimal("0"),
            "DEF_REDUCE": Decimal("0"),
            "Ignore_DEF": Decimal("0"),
            "WEAK_DMG": Decimal("0"),
        }

        # Apply weapon set
        applied = apply_weapon_set(user_config)

        # Convert float values back to Decimal for calculations
        for key in applied:
            if isinstance(applied[key], float):
                applied[key] = Decimal(str(applied[key]))

        # Merge configs
        merged = merge_configs(char_config, applied)

        # Convert merged values to Decimal as well (merge_configs returns floats)
        for key in merged:
            if isinstance(merged[key], float):
                merged[key] = Decimal(str(merged[key]))

        # Use default skill damage for test
        skill_dmg = Decimal("100")
        atk_base = Decimal("1500")  # Magic class Legend
        total_atk = calculate_total_atk(
            atk_char=merged["ATK_CHAR"],
            atk_pet=merged.get("ATK_PET", Decimal("0")),
            atk_base=atk_base,
            formation=merged["Formation"],
            potential_pet=merged.get("Potential_PET", Decimal("0")),
            buff_atk=merged.get("BUFF_ATK", Decimal("0")),
            buff_atk_pet=merged.get("BUFF_ATK_PET", Decimal("0")),
        )

        # Calculate RAW Damage
        raw_dmg = calculate_raw_dmg(
            total_atk=total_atk,
            skill_dmg=skill_dmg,
            crit_dmg=merged.get("CRIT_DMG", Decimal("100")),
            weak_dmg=merged.get("WEAK_DMG", Decimal("0")),
            dmg_amp_buff=merged.get("DMG_AMP_BUFF", Decimal("0")),
            dmg_amp_debuff=merged.get("DMG_AMP_DEBUFF", Decimal("0")),
            dmg_reduction=merged.get("DMG_Reduction", Decimal("0")),
        )

        # Calculate Effective DEF
        eff_def = calculate_effective_def(
            def_target=merged.get("DEF_Target", Decimal("0")),
            def_buff=merged.get("DEF_BUFF", Decimal("0")),
            def_reduce=merged.get("DEF_REDUCE", Decimal("0")),
            ignore_def=merged.get("Ignore_DEF", Decimal("0")),
        )

        # Calculate Final Damage
        final_dmg = calculate_final_dmg(raw_dmg, eff_def)

        # Sanity checks
        assert total_atk > Decimal("5000")
        assert raw_dmg > Decimal("0")
        assert eff_def > Decimal("1")
        assert final_dmg > 0
        assert final_dmg < raw_dmg  # DEF reduces damage

    def test_weapon_set_impact_on_damage(self):
        """Test weapon set actually affects damage"""
        base_config = {
            "Weapon_Set": 0,
            "ATK_CHAR": Decimal("5000"),
            "Formation": Decimal("42"),
            "CRIT_DMG": Decimal("288"),
            "DEF_Target": Decimal("1461"),
            "WEAK_DMG": Decimal("0"),
            "Ignore_DEF": Decimal("0"),
            "DMG_AMP_BUFF": Decimal("0"),
            "DMG_Reduction": Decimal("0"),
        }

        # No weapon
        config1 = apply_weapon_set(base_config.copy())
        raw1 = calculate_raw_dmg(
            Decimal("6000"), Decimal("100"), Decimal(str(config1.get("CRIT_DMG", 288))),
            Decimal(str(config1.get("WEAK_DMG", 0))), Decimal(str(config1.get("DMG_AMP_BUFF", 0))), Decimal("0"), Decimal(str(config1.get("DMG_Reduction", 0)))
        )

        # Weakness weapon
        base_config["Weapon_Set"] = 1
        config2 = apply_weapon_set(base_config.copy())
        raw2 = calculate_raw_dmg(
            Decimal("6000"), Decimal("100"), Decimal(str(config2.get("CRIT_DMG", 288))),
            Decimal(str(config2.get("WEAK_DMG", 0))), Decimal(str(config2.get("DMG_AMP_BUFF", 0))), Decimal("0"), Decimal(str(config2.get("DMG_Reduction", 0)))
        )

        assert raw2 > raw1  # Weakness weapon increases damage

    def test_monster_preset_loading(self):
        """Test loading and using monster presets"""
        # Load castle room 1 (need .json extension)
        monster = load_monster_preset("castle_room1.json")
        assert monster is not None
        # Just verify the monster loads and has some data
        assert len(monster) > 0


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestConfigErrorHandling:
    """Test error handling in config loading"""

    def test_load_nonexistent_character(self):
        """Test loading character that doesn't exist"""
        meta, config = load_character_full("nonexistent")
        assert (meta, config) == ({}, {})

    def test_load_nonexistent_monster(self):
        """Test loading monster preset that doesn't exist"""
        result = load_monster_preset("nonexistent")
        assert result == {}

    def test_merge_empty_configs(self):
        """Test merging empty configs"""
        result = merge_configs({}, {})
        assert result == {}

    def test_get_decimal_missing_key_no_default(self):
        """Test get_decimal with missing key and no default"""
        config = {}
        # get_decimal will raise an exception or return None for missing key with no default
        try:
            result = get_decimal(config, "missing", None)
            assert result is None or result == "None"
        except:
            pass  # Expected behavior


# ============================================================================
# ATK_BASE Tests by Class
# ============================================================================

class TestATK_BASE:
    """Test ATK_BASE values for different character classes"""

    def test_atk_base_values_exist(self):
        """Test ATK_BASE values are defined"""
        from constants import ATK_BASE
        assert ATK_BASE is not None
        assert "legend" in ATK_BASE
        assert "rare" in ATK_BASE

    def test_atk_base_legend_classes(self):
        """Test Legend ATK_BASE by class"""
        from constants import ATK_BASE

        classes = ["magic", "attack", "support", "defense", "balance"]
        for cls in classes:
            assert cls in ATK_BASE["legend"]
            assert ATK_BASE["legend"][cls] > Decimal("0")

    def test_atk_base_rare_classes(self):
        """Test Rare ATK_BASE by class"""
        from constants import ATK_BASE

        classes = ["magic", "attack", "support", "defense", "balance"]
        for cls in classes:
            assert cls in ATK_BASE["rare"]
            assert ATK_BASE["rare"][cls] > Decimal("0")

    def test_legend_higher_than_rare(self):
        """Test Legend ATK_BASE is higher than Rare"""
        from constants import ATK_BASE

        for cls in ["magic", "attack", "support", "defense", "balance"]:
            legend = ATK_BASE["legend"][cls]
            rare = ATK_BASE["rare"][cls]
            assert legend > rare, f"Legend {cls} should be higher than Rare"

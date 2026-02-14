"""
Pytest Configuration and Shared Fixtures
"""

import pytest
import sys
from pathlib import Path
from decimal import Decimal


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower, dependencies)"
    )
    config.addinivalue_line(
        "markers", "edge: Edge case and boundary tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow-running tests"
    )


# ============================================================================
# Shared Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def calculator_path():
    """Path to calculator directory"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def test_data_path(calculator_path):
    """Path to test data directory"""
    return calculator_path / "tests" / "fixtures"


@pytest.fixture(scope="session")
def characters_path(calculator_path):
    """Path to characters directory"""
    return calculator_path / "characters"


@pytest.fixture
def standard_atk_config():
    """Standard ATK configuration for testing"""
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
def standard_damage_config():
    """Standard damage configuration for testing"""
    return {
        "total_atk": Decimal("5400"),
        "skill_dmg": Decimal("160"),
        "crit_dmg": Decimal("288"),
        "weak_dmg": Decimal("65"),
        "dmg_amp_buff": Decimal("0"),
        "dmg_amp_debuff": Decimal("0"),
        "dmg_reduction": Decimal("10"),
    }


@pytest.fixture
def standard_def_config():
    """Standard DEF configuration for testing"""
    return {
        "def_target": Decimal("1461"),
        "def_buff": Decimal("0"),
        "def_reduce": Decimal("0"),
        "ignore_def": Decimal("0"),
    }


# ============================================================================
# Helper Functions
# ============================================================================

def approx_decimal(value: Decimal, tolerance: Decimal = Decimal("1")) -> bool:
    """
    Compare Decimal values with tolerance

    Args:
        value: First value
        tolerance: Maximum difference allowed

    Returns:
        True if values are within tolerance
    """
    def approx(a: Decimal, b: Decimal, tol: Decimal = Decimal("1")) -> bool:
        return abs(a - b) <= tol

    return pytest.approx(float(value), abs=float(tolerance))


# ============================================================================
# Test Data
# ============================================================================

@pytest.fixture
def atk_base_values():
    """ATK_BASE values by class and rarity"""
    return {
        "legend": {
            "magic": Decimal("1500"),
            "attack": Decimal("1500"),
            "support": Decimal("1095"),
            "defense": Decimal("727"),
            "balance": Decimal("1306"),
        },
        "rare": {
            "magic": Decimal("1389"),
            "attack": Decimal("1389"),
            "support": Decimal("1035"),
            "defense": Decimal("704"),
            "balance": Decimal("1238"),
        },
    }


@pytest.fixture
def castle_monster_data():
    """Castle monster preset data"""
    return {
        "room1": {
            "name": "Castle Room 1",
            "def": Decimal("689"),
            "hp": Decimal("8650"),
        },
        "room2": {
            "name": "Castle Room 2",
            "def": Decimal("784"),
            "hp": Decimal("10790"),
        },
    }


@pytest.fixture
def weapon_set_bonuses():
    """Weapon set bonuses"""
    return {
        0: {"name": "None", "weak_dmg": 0, "ignore_def": 0, "dmg_amp": 0},
        1: {"name": "Weakness", "weak_dmg": 35, "ignore_def": 0, "dmg_amp": 0},
        2: {"name": "Crit", "weak_dmg": 0, "ignore_def": 15, "dmg_amp": 0},
        3: {"name": "Hydra", "weak_dmg": 0, "ignore_def": 0, "dmg_amp": 70},
        4: {"name": "Hydra Castle", "weak_dmg": 0, "ignore_def": 0, "dmg_amp": 30},
    }

# 7k Rebirth Damage Calculator - Test Strategy

> **Project Type:** CLI Application with Critical Mathematical Calculations
> **Test Framework:** pytest
> **Python Version:** 3.10+
> **Last Updated:** 2026-02-07

---

## 📋 Executive Summary

This document outlines the comprehensive test strategy for the 7k Rebirth Damage Calculator. The calculator performs precise damage calculations for a game, where accuracy is critical.

**Risk Assessment:**
- **Critical Risk:** Formula accuracy errors produce incorrect damage values
- **High Risk:** Config merging bugs cause wrong character stats
- **Medium Risk:** Edge cases (overflow, division by zero)
- **Low Risk:** UI/display issues (cosmetic only)

---

## 🎯 Test Objectives

1. **Formula Accuracy:** Ensure all damage formulas match game mechanics exactly
2. **Regression Prevention:** Catch formula changes that break expected outputs
3. **Edge Case Coverage:** Handle boundary values and invalid inputs
4. **Character Coverage:** Test all 11 characters (standard + special)
5. **Integration Validation:** Verify config merging, registry pattern, weapon sets

---

## 📊 Test Coverage Matrix

### Current Coverage vs. Target

| Module | Current | Target | Priority |
|--------|---------|--------|----------|
| `damage_calc.py` | ❌ 0% | ✅ 100% | 🔴 CRITICAL |
| `config_loader.py` | ❌ 0% | ✅ 80% | 🟡 HIGH |
| `character_registry.py` | ❌ 0% | ✅ 60% | 🟡 MEDIUM |
| Special Character Logic | 🟡 Manual | ✅ Automated | 🟡 HIGH |
| Standard Characters | ❌ 0% | ✅ 80% | 🟡 MEDIUM |
| `menu.py` | ❌ 0% | ✅ 20% | 🟢 LOW |
| `display.py` | ❌ 0% | ✅ 10% | 🟢 LOW |

---

## 🧪 Test Categories

### 1. Unit Tests - `test_damage_calc.py`

**Purpose:** Test core calculation functions in isolation

**Test Cases:**

#### A. `calculate_total_atk()`
| Test Case | Description | Expected |
|-----------|-------------|----------|
| Base calculation | Basic ATK computation | Correct total |
| Formation bonus | Formation > 0 | Increases ATK |
| Potential pet | Potential_PET > 0 | Increases ATK |
| Buff stacking | BUFF_ATK + BUFF_ATK_PET | Multiplicative |
| Zero values | All inputs = 0 | Returns 0 |
| Negative values | Negative ATK | Should handle/raise |

#### B. `calculate_raw_dmg()`
| Test Case | Description | Expected |
|-----------|-------------|----------|
| Base damage | Standard inputs | Correct RAW |
| Weakness hit | WEAK_DMG > 0 | Increased damage |
| Crit + Weakness | Both modifiers | Combined effect |
| DMG_AMP stacking | BUFF + DEBUFF | Correct multiplier |
| HP-based damage | Final_DMG_HP > 0 | Added to base |
| DMG_Reduction | Reduction active | Decreases damage |

#### C. `calculate_effective_def()`
| Test Case | Description | Expected |
|-----------|-------------|----------|
| Base DEF | Standard DEF | > 1.0 |
| DEF_BUFF | Buff active | Higher DEF |
| DEF_REDUCE | Reduce active | Lower DEF |
| Ignore_DEF | Ignore active | Lower DEF |
| All modifiers | All stacked | Correct combined |

#### D. `calculate_final_dmg()`
| Test Case | Description | Expected |
|-----------|-------------|----------|
| Rounding | .5 values | Rounds DOWN |
| Zero damage | RAW = 0 | Returns 0 |
| Large values | 10M+ damage | Correct result |

#### E. HP-Based Functions
| Function | Test Case | Expected |
|----------|-----------|----------|
| `calculate_dmg_hp()` | 7% of 10,000 HP | 700 |
| `calculate_cap_atk()` | 100% of 5,000 ATK | 5,000 |
| `calculate_final_dmg_hp()` | Exceeds cap | Capped value |
| `calculate_final_dmg_hp()` | Under cap | Actual value |

---

### 2. Integration Tests - `test_characters.py`

**Purpose:** Test character-specific logic end-to-end

**Test Cases:**

#### A. Special Characters (Must Match Showcase)
| Character | Test | Expected Value |
|-----------|------|----------------|
| **Biscuit** | DEF_BASE import | 675 |
| **Biscuit** | Formation bonus | 70.875 |
| **Freyja** | HP Alteration 39% | 61,000,000 |
| **Espada** | HP-Based 7% | Correct increase |
| **Ryan** | Lost HP 30% left | +35% bonus |

#### B. Standard Characters
| Character | Test | Expected |
|-----------|------|----------|
| Miho | Standard calculation | No errors |
| Pascal | Bonus Crit DMG mapping | CRIT_DMG added |
| Rachel | DEF_REDUCE + DMG_AMP | Correct multipliers |
| Teo | Standard calculation | No errors |
| Yeonhee | HP-Based calculation | Correct values |

---

### 3. Edge Case Tests - `test_edge_cases.py`

**Purpose:** Handle boundary values and invalid inputs

**Test Cases:**

| Category | Test Case | Expected Behavior |
|----------|-----------|-------------------|
| **Zero Values** | ATK_CHAR = 0 | Returns 0 |
| **Zero Values** | CRIT_DMG = 0 | Returns 0 |
| **Zero Values** | SKILL_DMG = 0 | Returns 0 |
| **Negative** | Negative ATK | Raise error or handle |
| **Overflow** | ATK > 1,000,000 | Correct calculation |
| **Precision** | Decimal(0.1) + Decimal(0.2) | Exactly 0.3 |
| **Division** | DEF_Target = 0 | Handle gracefully |
| **Rounding** | 100.5 damage | Returns 100 (not 101) |

---

### 4. Config Tests - `test_config.py`

**Purpose:** Verify config loading and merging

**Test Cases:**

| Test Case | Description | Expected |
|-----------|-------------|----------|
| Load character | Load valid JSON | Returns dict |
| Load monster | Load monster preset | Returns dict |
| Merge additive | SKILL_DMG: 100 + 50 | 150 |
| Merge mapping | Bonus_Crit_DMG → CRIT_DMG | Added to CRIT_DMG |
| Weapon Set 0 | No weapon | No bonus |
| Weapon Set 1 | Weakness | WEAK_DMG += 35 |
| Weapon Set 2 | Crit | Ignore_DEF += 15 |
| Weapon Set 3 | Hydra | DMG_AMP_BUFF += 70 |
| Invalid JSON | Malformed JSON | Raise error |

---

### 5. Registry Tests - `test_registry.py`

**Purpose:** Verify registry pattern works correctly

**Test Cases:**

| Test Case | Description | Expected |
|-----------|-------------|----------|
| Register character | @register_character | Added to registry |
| Get handler | Get registered character | Returns function |
| List characters | List all registered | Returns list |
| Duplicate register | Register same name | Raise error |
| Unknown character | Get unregistered | Returns None |

---

## 🔬 Property-Based Testing

Using `hypothesis` for invariant testing:

```python
@given(st.decimals(min_value=0, max_value=10000))
def test_damage_never_negative(atk_value):
    """Damage should never be negative"""
    result = calculate_total_atk(...)
    assert result >= 0

@given(st.decimals(min_value=0, max_value=2000))
def test_effective_def_greater_than_one(def_target):
    """Effective DEF should always be > 1"""
    result = calculate_effective_def(def_target, ...)
    assert result > 1
```

---

## 📈 Test Metrics

### Coverage Goals
- **Line Coverage:** 90%+
- **Branch Coverage:** 85%+
- **Critical Path Coverage:** 100%

### CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install pytest pytest-cov
      - run: pytest --cov=calculator --cov-report=xml
```

---

## 🚦 Test Execution

### Run All Tests
```bash
pytest calculator/tests/ -v
```

### Run with Coverage
```bash
pytest calculator/tests/ --cov=calculator --cov-report=html
```

### Run Specific Category
```bash
pytest calculator/tests/test_damage_calc.py -v
pytest calculator/tests/test_characters.py -v
```

### Run Edge Cases Only
```bash
pytest calculator/tests/test_edge_cases.py -v
```

---

## 📝 Test Data Management

### Fixtures
Located in `tests/fixtures/`:
- `test_characters.json` - Test character data
- `test_monsters.json` - Test monster presets
- `expected_outputs.json` - Expected results from showcase

### Mock Data
Use `pytest.fixture` for reusable test data:
```python
@pytest.fixture
def standard_config():
    return {
        "ATK_CHAR": Decimal("5000"),
        "CRIT_DMG": Decimal("288"),
        ...
    }
```

---

## 🔄 Regression Testing

### Before Release
1. Run full test suite
2. Verify showcase values match
3. Run edge case tests
4. Check coverage report

### After Code Changes
1. Run affected module tests
2. Run integration tests
3. Verify no regression in showcase outputs

---

## 🐛 Bug Testing Protocol

When a bug is found:
1. **Reproduce:** Create failing test case
2. **Isolate:** Determine root cause
3. **Fix:** Implement fix
4. **Verify:** Test now passes
5. **Prevent:** Add regression test

---

## 📚 Test Documentation

### Test Case Template
```python
def test_<function>_<scenario>():
    """
    Test: <what is being tested>
    Given: <initial conditions>
    When: <action taken>
    Then: <expected result>
    """
    # Arrange
    input_data = ...

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_value
```

---

## ✅ Definition of Done

A feature is "test complete" when:
- ✅ All unit tests pass (100%)
- ✅ Integration tests pass (100%)
- ✅ Edge cases covered
- ✅ Showcase values verified
- ✅ Coverage threshold met (90%+)
- ✅ No regressions in existing tests

---

## 📞 Contact

For questions about this test strategy, please refer to:
- `AGENTS.md` - AI agent guide
- `README.md` - User documentation
- `SHOWCASES.md` - Expected output examples

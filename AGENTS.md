# 7k Rebirth Damage Calculator - AI Agent Guide

> 🎮 **Game:** Seven Knights Rebirth  
> 🎯 **Purpose:** Calculate precise skill damage  
> 📁 **Project:** `calculator/` (Python CLI)
> 🐍 **Python:** 3.10+ (with full type hints)

---

## 🚀 Quick Start

```bash
cd calculator
python main.py
```

1. Select mode (Standard / Castle Rush / ATK Compare)
2. Select character (or ATK_BASE for compare mode)
3. Select skill (or enter comparison values)
4. View results

**Files to modify:**
- `config.json` - User values (ATK, CRIT_DMG, Weapon_Set, etc.)
- `characters/*.json` - Character data
- `characters/monster/*.json` - Monster DEF/HP values

---

## 📁 File Structure (Refactored)

```
7k-project/
├── AGENTS.md            # This file - AI Agent guide
├── README.md            # User-facing documentation
├── GAMEWITH_GUIDE.md    # Guide for scraping GameWith data
├── docs/
│   └── SHOWCASES.md     # Character output examples
└── calculator/
    ├── main.py              # Entry Point - orchestrates all modules
    ├── config_loader.py     # Load and merge config files
    ├── menu.py              # UI/Menu selection (mode, character, skill)
    ├── display.py           # All display/output functions
    ├── damage_calc.py       # Core calculation formulas
    ├── constants.py         # Constants (DEF_MODIFIER, ATK_BASE)
    ├── config.json          # User settings
    ├── characters/          # Character files
    │   ├── espada.json
    │   ├── freyja.json
    │   ├── klahan.json
    │   ├── miho.json
    │   ├── pascal.json
    │   ├── rachel.json
    │   ├── ryan.json
    │   ├── sun_wukong.json
    │   ├── teo.json
    │   ├── yeonhee.json
    │   └── monster/         # Monster presets
    │       ├── castle_room1.json  # DEF=689, HP=8,650
    │       ├── castle_room2.json  # DEF=784, HP=10,790
    │       └── normal.json
    └── logic/               # Special logic (complex characters)
        ├── espada.py        # HP-Based + Multi-scenario
        ├── freyja.py        # HP Alteration
        ├── klahan.py        # HP Condition Bonus
        ├── ryan.py          # Lost HP Bonus + Weakness Extra
        └── sun_wukong.py    # Castle Mode (min crits needed)
```

---

## 🔒 Type Hints (Python 3.10+)

All files have complete type hints for:
- Better IDE autocomplete and error detection
- Self-documenting code
- Prevent runtime errors

### Features Used:
```python
from __future__ import annotations  # Modern type hints
from typing import Any              # Generic types
from decimal import Decimal         # Precision math

# Example function signature:
def calculate_damage(
    total_atk: Decimal,
    skill_dmg: Decimal,
    crit_dmg: Decimal
) -> dict[str, Any]:
    ...
```

### Type Aliases:
```python
# damage_calc.py
NumericType = Union[int, float, str, Decimal]  # Values that can be Decimal
```

---

## 🧩 Module Responsibilities

### `main.py` - Entry Point
- Orchestrates all modules
- Flow sequence: mode → character → skill → calculate → display
- Checks if special logic is needed

### `config_loader.py` - Config Management
| Function | Description |
|----------|-------------|
| `list_characters()` | List character names in `characters/` |
| `load_json(path)` | Load JSON, filter comments/metadata |
| `load_character_full(name)` | Load character with metadata |
| `load_user_config()` | Load `config.json` |
| `load_monster_preset(filename)` | Load monster preset |
| `apply_weapon_set(config)` | Apply weapon set bonuses |
| `merge_configs(char, user)` | Merge configs by ADD values |
| `get_decimal(config, key, default)` | Get value as Decimal |

### `menu.py` - UI/Menu Selection
| Function | Description |
|----------|-------------|
| `select_mode()` | Select mode (Standard/Castle/ATK Compare) |
| `select_character()` | Select character → return (name, meta, config) |
| `select_skill(meta)` | Select skill → return (config, is_both, all_skills) |
| `select_atk_base()` | Select ATK_BASE (Legend/Rare/Custom) |
| `input_compare_values(config)` | Enter comparison values (Formation, ATK_CHAR) |

### `display.py` - Output Functions
| Function | Description |
|----------|-------------|
| `print_header()` | Display program header |
| `print_character_info()` | Display character info |
| `print_weapon_set()` | Display weapon set |
| `print_input_values()` | Display all input values |
| `print_calculation_header()` | Display calculation header |
| `print_total_atk()` | Display Total ATK |
| `print_hp_based_damage()` | Display HP-Based Damage |
| `print_raw_damage()` | Display RAW Damage |
| `print_effective_def()` | Display Effective DEF |
| `print_final_damage_results()` | Display Final Damage results |
| `print_espada_results()` | Display Espada special results |
| `print_both_skills_results()` | Display combined skills results |
| `get_hp_status()` | Generate monster HP status text |
| `calc_atk_needed()` | Calculate ATK needed to kill monster |

### `damage_calc.py` - Core Calculation
| Function | Description |
|----------|-------------|
| `calculate_total_atk()` | Calculate Total ATK |
| `calculate_dmg_hp()` | Calculate DMG from HP |
| `calculate_cap_atk()` | Calculate Cap ATK |
| `calculate_final_dmg_hp()` | Calculate Final DMG HP |
| `calculate_raw_dmg()` | Calculate RAW Damage |
| `calculate_effective_def()` | Calculate Effective DEF |
| `calculate_final_dmg()` | Calculate Final Damage |

### `constants.py` - Constants
| Constant | Value | Note |
|----------|-------|------|
| `DEF_MODIFIER` | 0.00214135 | DEF multiplier |
| `ATK_BASE["legend"]["magic"]` | 1500 | Magic class Legend |
| `ATK_BASE["legend"]["attack"]` | 1500 | Attack class Legend |
| `ATK_BASE["legend"]["support"]` | 1095 | Support class Legend |
| `ATK_BASE["legend"]["defense"]` | 727 | Defense class Legend |
| `ATK_BASE["legend"]["balance"]` | 1306 | Balance class Legend |

---

## 📐 Core Formulas

### 1. Total ATK
```
Total_ATK = (ATK_CHAR + ATK_PET + ATK_BASE × (Formation + Potential_PET)/100) 
            × (1 + (BUFF_ATK + BUFF_ATK_PET)/100)
```

### 2. RAW Damage
```
RAW_DMG = Total_ATK × SKILL_DMG/100 × CRIT_DMG/100 
          × (1 + WEAK_DMG/100) × (1 + DMG_AMP_BUFF/100) 
          × (1 + (DMG_AMP_DEBUFF - DMG_Reduction)/100)
          + Final_DMG_HP × [same multipliers]
```

### 3. Effective DEF
```
Effective_DEF = 1 + DEF_Modifier × DEF_Target 
                × (1 + DEF_BUFF/100 - DEF_REDUCE/100) 
                × (1 - Ignore_DEF/100)
```
> **DEF_Modifier = 0.00214135** (constant)

### 4. Final Damage
```
Final_DMG = ROUNDDOWN(RAW_DMG / Effective_DEF) × SKILL_HITS
```

---

## 🎯 Weakness Hit

```
WEAK_DMG_Total = 30% (base) + WEAK_DMG (from config/character)
```

> ⚠️ **Important:** When hitting weakness, there's always a base 30%, then +WEAK_DMG

---

## 🗡️ Weapon Sets

```python
Weapon_Set = 0  # None
Weapon_Set = 1  # Weakness: WEAK_DMG += 35
Weapon_Set = 2  # Crit: Ignore_DEF += 15
Weapon_Set = 3  # Hydra: DMG_AMP_BUFF += 70
Weapon_Set = 4  # Hydra Castle: DMG_AMP_BUFF += 30
```

**Implementation in `config_loader.py` → `apply_weapon_set()`**

---

## ⚔️ Special Mechanics (Logic Files)

### HP Alteration (Freyja) - `logic/freyja.py`
> Directly reduces target HP to X%

```python
damage = HP_Target × (100 - HP_Alteration) / 100
# Example: 100,000 HP × 0.61 = 61,000 damage (monster left at 39%)
```

| Field | Value | Note |
|-------|-------|------|
| `HP_Alteration` | 39.00 | Monster left at 39% |

**Functions:**
- `calculate_hp_alteration_damage()` - Calculate HP Alteration damage
- `calculate_freyja_damage()` - Calculate all 4 cases
- `print_freyja_results()` - Display results

---

### Lost HP Bonus (Ryan) - `logic/ryan.py`
> Damage increases based on % HP target has lost

```python
lost_hp = 100 - Target_HP_Percent
bonus = Lost_HP_Bonus × lost_hp / 100
final = base_damage × (1 + bonus/100)
# Example: Lost_HP_Bonus=50%, HP left 30% → +35% damage
```

| Field | Value | Note |
|-------|-------|------|
| `Lost_HP_Bonus` | 50.00 | Max +50% |
| `Target_HP_Percent` | 30.00 | Target HP left at 30% |
| `WEAK_SKILL_DMG` | 270.00 | Extra damage on weakness hit |

**Functions:**
- `calculate_lost_hp_multiplier()` - Calculate Lost HP multiplier
- `calculate_ryan_damage()` - Calculate all 4 cases
- `print_ryan_results()` - Display results

---

### HP Condition Bonus (Klahan) - `logic/klahan.py`
> Damage increases when HP meets condition

```python
if HP >= 50%: SKILL_DMG += HP_Above_50_Bonus
if HP <= 50%: SKILL_DMG += HP_Below_50_Bonus
```

| Field | Condition | Value |
|-------|-----------|-------|
| `HP_Above_50_Bonus` | HP ≥ 50% | +135% |
| `HP_Below_50_Bonus` | HP ≤ 50% | +115% |

**Functions:**
- `calculate_klahan_damage()` - Calculate all 4 cases
- `print_klahan_results()` - Display results

---

### HP-Based Damage (Espada) - `logic/espada.py`
> Damage increases based on % of target Max HP

```python
dmg_hp = HP_Target × Bonus_DMG_HP_Target / 100
cap = Total_ATK × Cap_ATK_Percent / 100
final_hp = min(dmg_hp, cap) if cap > 0 else dmg_hp
```

| Field | Value | Note |
|-------|-------|------|
| `Bonus_DMG_HP_Target` | 7.00 | 7% of Max HP |
| `Cap_ATK_Percent` | 100.00 | Cap at 100% ATK |

**Functions:**
- `calculate_espada_damage()` - Calculate 4 cases (crit/weakness × with/without HP-based)

---

### Castle Mode (Sun Wukong) - `logic/sun_wukong.py`
> Calculate minimum crits needed to kill monster

**Assumption:** All hits apply weakness, but some hits may also crit

```python
# Damage per hit:
# - Weakness only: dmg_weak = CRIT_DMG=100%, WEAK_DMG=30%+config
# - Crit + Weakness: dmg_crit = CRIT_DMG=user%, WEAK_DMG=30%+config

# Formula: c hits crit + (n-c) hits weakness only
total_dmg = (c * dmg_crit) + ((n - c) * dmg_weak)
```

**Functions:**
- `calculate_sun_wukong_castle_mode()` - Calculate all scenarios
- `print_castle_mode_results()` - Display table + min crits summary

**Output:**
```
🎲 Damage Table by Crit Count
   Crit  Weakness     Total DMG     Result
     0       3        16,461      ☠️ Dead ⬅️ MIN
     1       3        25,131      ☠️ Dead
```

---

### Bonus Crit DMG (Teo)
> Crit DMG bonus from skill (auto-add via mapping)

```python
CRIT_DMG = user_CRIT_DMG + Bonus_Crit_DMG
# Example: 288% + 85% = 373%
```

| Field | Value | Note |
|-------|-------|------|
| `Bonus_Crit_DMG` | 85.00 | Added to CRIT_DMG |

**Implementation:** Uses `mapping_keys` in `config_loader.py` → `merge_configs()`

---

## 🔄 Config Merging Logic

### Additive Keys (character + user = final)
```python
additive_keys = [
    "SKILL_DMG", "CRIT_DMG", "WEAK_DMG", "DMG_AMP_BUFF", "DMG_AMP_DEBUFF",
    "DEF_REDUCE", "BUFF_ATK", "DMG_Reduction", "Ignore_DEF",
    "Bonus_DMG_HP_Target", "Cap_ATK_Percent"
]
```

### Mapping Keys (source → target)
```python
mapping_keys = {"Bonus_Crit_DMG": "CRIT_DMG"}
```

**Implementation:** `config_loader.py` → `merge_configs()`

---

## 📋 Character JSON Template

```json
{
    "_character": "Name",
    "_rarity": "legend",
    "_class": "magic",
    "_element": "Dark",
    "_source": "https://gamewith.net/...",
    
    "BUFF_ATK": 0.00,
    "CRIT_DMG": 0.00,
    "DMG_AMP_BUFF": 0.00,
    "WEAK_DMG": 0.00,
    
    "_skills": {
        "skill1": {
            "_name": "Skill Name (Top)",
            "SKILL_DMG": 100.00,
            "SKILL_HITS": 1,
            "Ignore_DEF": 0.00,
            "Bonus_DMG_HP_Target": 0.00,
            "Cap_ATK_Percent": 0.00
        },
        "skill2": {
            "_name": "Skill Name (Bottom)",
            "SKILL_DMG": 100.00,
            "SKILL_HITS": 1
        }
    },
    
    "_notes": ["Enhanced values"]
}
```

### Metadata Keys (prefixed with `_`)
| Key | Description |
|-----|-------------|
| `_character` | Character name |
| `_rarity` | legend / rare |
| `_class` | attack / magic / support / defense / balance |
| `_element` | Fire / Water / Light / Dark / Wind |
| `_source` | Data source URL |
| `_skills` | Object containing skill data |
| `_notes` | Notes |

---

## 🐉 Monster Presets

### `characters/monster/castle_room1.json`
```json
{
    "_mode": "castle",
    "_name": "Castle Room 1",
    "DEF_Target": 689.00,
    "HP_Target": 8650.00,
    "Target_HP_Percent": 0.00,
    "DMG_Reduction": 0.00,
    "DEF_BUFF": 0.00
}
```

### `characters/monster/castle_room2.json`
```json
{
    "_mode": "castle",
    "_name": "Castle Room 2",
    "DEF_Target": 784.00,
    "HP_Target": 10790.00,
    "Target_HP_Percent": 0.00,
    "DMG_Reduction": 0.00,
    "DEF_BUFF": 0.00
}
```

---

## ⚙️ config.json Template

```json
{
    "Weapon_Set": 3,           // 0-4 (see Weapon Sets table)
    "Formation": 42.00,        // % Formation bonus
    "ATK_CHAR": 4488.00,       // ATK value shown in game
    "CRIT_DMG": 288.00,        // % Crit Damage
    "DMG_AMP_BUFF": 0.00,      // % DMG AMP (from ring/buff)
    "ATK_PET": 391.00,         // Pet ATK
    "BUFF_ATK_PET": 19.00,     // % Pet ATK Buff
    "Potential_PET": 0.00,     // % Pet Potential
    "DEF_Target": 1461.00,     // Enemy DEF
    "HP_Target": 17917.00,     // Enemy HP
    "Target_HP_Percent": 30.00,// HP% left (for Lost HP Bonus)
    "DMG_Reduction": 10.00,    // % Enemy DMG Reduction
    "DEF_BUFF": 0.00           // % Enemy DEF Buff
}
```

---

## 🎮 ATK_BASE Reference

| Rarity | Magic | Attack | Defense | Support | Balance |
|--------|-------|--------|---------|---------|---------|
| Legend | 1500 | 1500 | 727 | 1095 | 1306 |
| Rare | 1389 | 1389 | 704 | 1035 | 1238 |

**Implementation:** `constants.py` → `ATK_BASE` dict and `get_atk_base()`

---

## 🐛 Lessons Learned / Gotchas

### 1. Weakness Damage = Base 30% + WEAK_DMG
> ⚠️ **Very Important!** When hitting weakness, it's not just +WEAK_DMG, you must add the base 30%

```python
# ❌ Wrong
weak_bonus = WEAK_DMG  # e.g. 35%

# ✅ Correct  
weak_bonus = 30 + WEAK_DMG  # 30% (base) + 35% = 65%
```

**Lesson:** In-game damage is `crit_damage × 1.65` (not ×1.35)

---

### 2. Multi-Hit: Final Damage is "Per Hit" not Total
> ⚠️ **Don't confuse!** Formula calculates damage **per hit**, then multiply by SKILL_HITS

```python
# ❌ Wrong - divide by hits first
final_per_hit = ROUNDDOWN(raw_dmg / eff_def) / skill_hits

# ✅ Correct - damage per hit then multiply
final_per_hit = ROUNDDOWN(raw_dmg / eff_def)
total_damage = final_per_hit × skill_hits
```

**Lesson:** When comparing with game (e.g. 2,688) → must know if it's "per hit" or "total"

---

### 3. DMG_Reduction is in RAW_DMG not Final
> ⚠️ **DMG_Reduction is subtracted in RAW step**, not after dividing by DEF

```python
# Correct formula (in RAW_DMG)
raw_dmg = ... × (1 + (DMG_AMP_DEBUFF - DMG_Reduction)/100)

# ❌ Not like this
final = raw_dmg / eff_def × (1 - DMG_Reduction/100)
```

---

### 4. Config Merge: Additive Keys Must Be Added
> ⚠️ **Values from character + user must ADD**, not overwrite

```python
# Example: Miho passive WEAK_DMG=23, user config=35
final_WEAK_DMG = 23 + 35 = 58
```

**Lesson:** If result is wrong → check if merge is correct

---

### 5. Windows Console Thai Encoding
> ⚠️ **Windows CMD doesn't support UTF-8 Thai** must add:

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
```

**Implementation:** `main.py` lines 9-11

---

### 6. Testing: Must Know Target Value from Game
> 📌 **Before testing, must know:**
> - In-game damage (e.g. 2,688)
> - Is it **per hit** or **total**
> - Is it **crit** or **weakness hit**
> - **Which skill** (top/bottom)

**Lesson:** Most common mistake is not knowing what value the game displays

---

## 👾 Supported Characters

| Character | Element | Class | Special Mechanics | Logic File |
|-----------|---------|-------|-------------------|------------|
| Espada | Fire | Magic | HP-Based + Multi-scenario | `logic/espada.py` |
| Freyja | Light | Magic | HP Alteration | `logic/freyja.py` |
| Klahan | Wind | Attack | HP Condition Bonus | `logic/klahan.py` |
| Miho | Water | Magic | Standard | - |
| Pascal | Dark | Magic | Standard | - |
| Rachel | Fire | Magic | DEF_REDUCE, DMG_AMP_DEBUFF | - |
| Ryan | Dark | Attack | Lost HP + Weakness Extra | `logic/ryan.py` |
| Sun Wukong | Fire | Balance | Castle Mode (min crits) | `logic/sun_wukong.py` |
| Teo | Dark | Attack | Bonus Crit DMG | - |
| Yeonhee | Dark | Magic | HP-Based | - |

---

## 🧠 AI Agent Instructions

### Adding New Characters

1. **Get data from GameWith** → Use Enhanced values
2. **Create JSON file** in `characters/`
3. **Decide if special logic is needed:**
   - Has HP Alteration? → Create `logic/[name].py`
   - Has HP condition bonus? → Add appropriate fields
   - Has Bonus Crit DMG? → Use automatic mapping
   - Has Lost HP Bonus? → Create logic file
4. **If has special logic:**
   - Create file in `logic/`
   - Add import and call in `main.py`
5. **Update `docs/SHOWCASES.md`:**
   - If has **special logic** → Add new showcase section
   - If **Standard** → Only add row to "Standard Characters" table
   - ⚠️ **Warning:** Don't add full showcase if no special mechanic (will be redundant)

### File Modification Guide

| Need to | Modify File |
|---------|-------------|
| Add/edit UI/Menu | `menu.py` |
| Add/edit display | `display.py` |
| Add/edit config loading | `config_loader.py` |
| Add/edit formulas | `damage_calc.py` |
| Add/edit constants | `constants.py` |
| Add special logic | `logic/[name].py` |
| Manage workflow | `main.py` |

### Testing
```bash
python main.py           # Interactive mode
```

---

## ⚠️ Important Notes

1. **All values are %** → Must `/100` in formulas
2. **ROUNDDOWN** → Damage always rounds down
3. **Base Weakness = 30%** → Added to WEAK_DMG
4. **Decimal** → Use Python Decimal for precision
5. **skill1 = Top, skill2 = Bottom** → Order in JSON
6. **Metadata keys prefixed with `_`** → Separated from config
7. **Comment keys prefixed with `//`** → Filtered out

---

## 🔗 Data Source

- **Primary:** [GameWith - Seven Knights Rebirth](https://gamewith.net/sevenknights-rebirth/)
- **Scraping Guide:** See `GAMEWITH_GUIDE.md` for data extraction instructions
- **Values:** Always use **Enhanced** (max values)
- **Transcend:** Specify in `_notes` if affects values

---

## 📝 Changelog

### 2026-01-25: ATK Compare Mode
- Changed mode 3 from "Calculate ATK only" to **"ATK Compare"**
- Added `input_compare_values()` function in `menu.py`
- Added `select_atk_base()` for selecting ATK_BASE (Legend/Rare/Custom)
- Display comparison between config.json and new input values

### 2026-01-24: Type Hints Refactor
- Added type hints to all files (100% coverage)
- Used `from __future__ import annotations` for modern syntax
- Added `NumericType` type alias in `damage_calc.py`
- Updated Python requirement to 3.10+

### 2026-01-20: Sun Wukong Castle Mode
- Added `logic/sun_wukong.py` - Castle Mode calculator
  - Calculate minimum crits needed to kill monster
  - Assumes all hits apply weakness, some hits may also crit
- Added `Weapon_Set = 4` Hydra Castle (DMG_AMP +30%)
- Updated AGENTS.md

### 2026-01-12: Major Refactor
- Split `main.py` (720 lines → ~300 lines) into:
  - `config_loader.py` - Load/merge config
  - `menu.py` - UI selection
  - `display.py` - Output functions
- Added monster presets for Castle mode
- Improved AGENTS.md completeness

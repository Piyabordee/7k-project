# 7k Rebirth Damage Calculator - AI Agent Guide

> 🎮 **เกม:** Seven Knights Rebirth  
> 🎯 **วัตถุประสงค์:** คำนวณดาเมจสกิลที่แม่นยำ  
> 📁 **โปรเจค:** `calculator/` (Python CLI)
> 🐍 **Python:** 3.10+ (with full type hints)

---

## 🚀 Quick Start

```bash
cd calculator
python main.py
```

1. เลือกโหมด (ปกติ / ตีปราสาท / เปรียบเทียบ ATK)
2. เลือกตัวละคร (หรือ ATK_BASE สำหรับโหมดเปรียบเทียบ)
3. เลือกสกิล (หรือกรอกค่าเปรียบเทียบ)
4. ดูผลลัพธ์

**ไฟล์ที่ต้องแก้:**
- `config.json` - ค่าผู้ใช้ (ATK, CRIT_DMG, Weapon_Set, ฯลฯ)
- `characters/*.json` - ข้อมูลตัวละคร
- `characters/monster/*.json` - ค่า DEF/HP มอนสเตอร์

---

## 📁 File Structure (Refactored)

```
calculator/
├── main.py              # Entry Point - ดึงทุก module มารัน
├── config_loader.py     # โหลดและ merge config files
├── menu.py              # UI/Menu selection (โหมด, ตัวละคร, สกิล)
├── display.py           # ฟังก์ชันแสดงผลทั้งหมด
├── damage_calc.py       # สูตรคำนวณหลัก
├── constants.py         # ค่าคงที่ (DEF_MODIFIER, ATK_BASE)
├── config.json          # ค่าผู้ใช้
├── characters/          # ไฟล์ตัวละคร
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
└── logic/               # Logic พิเศษ (ตัวละครที่ซับซ้อน)
    ├── espada.py        # HP-Based + Multi-scenario
    ├── freyja.py        # HP Alteration
    ├── klahan.py        # HP Condition Bonus
    ├── ryan.py          # Lost HP Bonus + Weakness Extra
    └── sun_wukong.py    # Castle Mode (คริขั้นต่ำ)
```

---

## 🔒 Type Hints (Python 3.10+)

ทุกไฟล์มี type hints ครบถ้วนสำหรับ:
- Better IDE autocomplete และ error detection
- Self-documenting code
- ป้องกัน runtime errors

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
- ดึงทุก module มารัน
- จัดลำดับ flow: โหมด → ตัวละคร → สกิล → คำนวณ → แสดงผล
- ตรวจสอบว่าต้องใช้ logic พิเศษหรือไม่

### `config_loader.py` - Config Management
| Function | หน้าที่ |
|----------|--------|
| `list_characters()` | แสดงรายชื่อตัวละครใน `characters/` |
| `load_json(path)` | โหลด JSON กรอง comment/metadata |
| `load_character_full(name)` | โหลด character รวม metadata |
| `load_user_config()` | โหลด `config.json` |
| `load_monster_preset(filename)` | โหลด monster preset |
| `apply_weapon_set(config)` | ใช้ชุดเซ็ทอาวุธ |
| `merge_configs(char, user)` | รวม config โดย ADD ค่า |
| `get_decimal(config, key, default)` | ดึงค่าเป็น Decimal |

### `menu.py` - UI/Menu Selection
| Function | หน้าที่ |
|----------|--------|
| `select_mode()` | เลือกโหมด (ปกติ/ตีปราสาท/เปรียบเทียบ ATK) |
| `select_character()` | เลือกตัวละคร → return (name, meta, config) |
| `select_skill(meta)` | เลือกสกิล → return (config, is_both, all_skills) |
| `select_atk_base()` | เลือก ATK_BASE (Legend/Rare/Custom) |
| `input_compare_values(config)` | กรอกค่าเปรียบเทียบ (Formation, ATK_CHAR) |

### `display.py` - Output Functions
| Function | หน้าที่ |
|----------|--------|
| `print_header()` | แสดง header โปรแกรม |
| `print_character_info()` | แสดงข้อมูลตัวละคร |
| `print_weapon_set()` | แสดงชุดเซ็ทอาวุธ |
| `print_input_values()` | แสดงค่า Input ทั้งหมด |
| `print_calculation_header()` | แสดง header ผลคำนวณ |
| `print_total_atk()` | แสดง Total ATK |
| `print_hp_based_damage()` | แสดง HP-Based Damage |
| `print_raw_damage()` | แสดง RAW Damage |
| `print_effective_def()` | แสดง Effective DEF |
| `print_final_damage_results()` | แสดงผล Final Damage |
| `print_espada_results()` | แสดงผล Espada พิเศษ |
| `print_both_skills_results()` | แสดงผลรวมทั้งสองสกิล |
| `get_hp_status()` | สร้างข้อความเลือดมอน |
| `calc_atk_needed()` | คำนวณ ATK ที่ต้องเพิ่มถึงจะฆ่ามอนได้ |

### `damage_calc.py` - Core Calculation
| Function | หน้าที่ |
|----------|--------|
| `calculate_total_atk()` | คำนวณ Total ATK |
| `calculate_dmg_hp()` | คำนวณ DMG จาก HP |
| `calculate_cap_atk()` | คำนวณ Cap ATK |
| `calculate_final_dmg_hp()` | คำนวณ Final DMG HP |
| `calculate_raw_dmg()` | คำนวณ RAW Damage |
| `calculate_effective_def()` | คำนวณ Effective DEF |
| `calculate_final_dmg()` | คำนวณ Final Damage |

### `constants.py` - Constants
| Constant | Value | Note |
|----------|-------|------|
| `DEF_MODIFIER` | 0.00214135 | ตัวคูณ DEF |
| `ATK_BASE["legend"]["magic"]` | 1500 | สายเวท Legend |
| `ATK_BASE["legend"]["attack"]` | 1500 | สายโจมตี Legend |
| `ATK_BASE["legend"]["support"]` | 1095 | สายซัพพอร์ต Legend |
| `ATK_BASE["legend"]["defense"]` | 727 | สายป้องกัน Legend |
| `ATK_BASE["legend"]["balance"]` | 1306 | สายสมดุล Legend |

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
> **DEF_Modifier = 0.00214135** (ค่าคงที่)

### 4. Final Damage
```
Final_DMG = ROUNDDOWN(RAW_DMG / Effective_DEF) × SKILL_HITS
```

---

## 🎯 Weakness Hit (ติดจุดอ่อน)

```
WEAK_DMG_Total = 30% (base) + WEAK_DMG (from config/character)
```

> ⚠️ **สำคัญ:** เมื่อติดจุดอ่อน มี base 30% เสมอ แล้วค่อย +WEAK_DMG

---

## 🗡️ Weapon Sets

```python
Weapon_Set = 0  # ไม่ใส่
Weapon_Set = 1  # จุดอ่อน: WEAK_DMG += 35
Weapon_Set = 2  # คริ: Ignore_DEF += 15
Weapon_Set = 3  # ไฮดร้า: DMG_AMP_BUFF += 70
Weapon_Set = 4  # ไฮดร้าตีปราสาท: DMG_AMP_BUFF += 30
```

**Implementation ใน `config_loader.py` → `apply_weapon_set()`**

---

## ⚔️ Special Mechanics (Logic Files)

### HP Alteration (Freyja) - `logic/freyja.py`
> ปรับ HP เป้าหมายเหลือ X% โดยตรง

```python
damage = HP_Target × (100 - HP_Alteration) / 100
# ตัวอย่าง: 100,000 HP × 0.61 = 61,000 damage (มอนเหลือ 39%)
```

| Field | Value | Note |
|-------|-------|------|
| `HP_Alteration` | 39.00 | มอนเหลือ 39% |

**Functions:**
- `calculate_hp_alteration_damage()` - คำนวณ HP Alteration damage
- `calculate_freyja_damage()` - คำนวณทั้ง 4 กรณี
- `print_freyja_results()` - แสดงผล

---

### Lost HP Bonus (Ryan) - `logic/ryan.py`
> ดาเมจเพิ่มตาม % HP ที่เป้าหมายเสียไป

```python
lost_hp = 100 - Target_HP_Percent
bonus = Lost_HP_Bonus × lost_hp / 100
final = base_damage × (1 + bonus/100)
# ตัวอย่าง: Lost_HP_Bonus=50%, HP เหลือ 30% → +35% damage
```

| Field | Value | Note |
|-------|-------|------|
| `Lost_HP_Bonus` | 50.00 | สูงสุด +50% |
| `Target_HP_Percent` | 30.00 | HP เป้าหมายเหลือ 30% |
| `WEAK_SKILL_DMG` | 270.00 | ดาเมจเสริมเมื่อติดจุดอ่อน |

**Functions:**
- `calculate_lost_hp_multiplier()` - คำนวณ Lost HP multiplier
- `calculate_ryan_damage()` - คำนวณทั้ง 4 กรณี
- `print_ryan_results()` - แสดงผล

---

### HP Condition Bonus (Klahan) - `logic/klahan.py`
> ดาเมจเพิ่มเมื่อ HP ตรงเงื่อนไข

```python
if HP >= 50%: SKILL_DMG += HP_Above_50_Bonus
if HP <= 50%: SKILL_DMG += HP_Below_50_Bonus
```

| Field | Condition | Value |
|-------|-----------|-------|
| `HP_Above_50_Bonus` | HP ≥ 50% | +135% |
| `HP_Below_50_Bonus` | HP ≤ 50% | +115% |

**Functions:**
- `calculate_klahan_damage()` - คำนวณทั้ง 4 กรณี
- `print_klahan_results()` - แสดงผล

---

### HP-Based Damage (Espada) - `logic/espada.py`
> ดาเมจเพิ่มตาม % ของ Max HP เป้าหมาย

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
- `calculate_espada_damage()` - คำนวณ 4 กรณี (คริ/จุดอ่อน × มี/ไม่มี HP-based)

---

### Castle Mode (Sun Wukong) - `logic/sun_wukong.py`
> คำนวณว่าต้องติดคริขั้นต่ำกี่ครั้งถึงมอนจะตาย

**สมมติ:** ทุก hit ติดจุดอ่อน แต่บาง hit อาจติดคริด้วย

```python
# ดาเมจต่อ hit:
# - ติดแค่จุดอ่อน: dmg_weak = CRIT_DMG=100%, WEAK_DMG=30%+config
# - ติดคริ+จุดอ่อน: dmg_crit = CRIT_DMG=user%, WEAK_DMG=30%+config

# สูตร: c hit ติดคริ + (n-c) hit ติดแค่จุดอ่อน
total_dmg = (c * dmg_crit) + ((n - c) * dmg_weak)
```

**Functions:**
- `calculate_sun_wukong_castle_mode()` - คำนวณทุก scenario
- `print_castle_mode_results()` - แสดงตาราง + สรุปคริขั้นต่ำ

**ผลลัพธ์:**
```
🎲 ตารางดาเมจตามจำนวนคริ
   คริ  จุดอ่อน      ดาเมจรวม     ผลลัพธ์
     0       3        16,461      ☠️ ตาย ⬅️ MIN
     1       3        25,131      ☠️ ตาย
```

---

### Bonus Crit DMG (Teo)
> Crit DMG bonus จากสกิล (auto-add via mapping)

```python
CRIT_DMG = user_CRIT_DMG + Bonus_Crit_DMG
# ตัวอย่าง: 288% + 85% = 373%
```

| Field | Value | Note |
|-------|-------|------|
| `Bonus_Crit_DMG` | 85.00 | ADD เข้า CRIT_DMG |

**Implementation:** ใช้ `mapping_keys` ใน `config_loader.py` → `merge_configs()`

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

### Metadata Keys (ขึ้นต้นด้วย `_`)
| Key | Description |
|-----|-------------|
| `_character` | ชื่อตัวละคร |
| `_rarity` | legend / rare |
| `_class` | attack / magic / support / defense / balance |
| `_element` | Fire / Water / Light / Dark / Wind |
| `_source` | URL แหล่งข้อมูล |
| `_skills` | Object เก็บข้อมูลสกิล |
| `_notes` | หมายเหตุ |

---

## 🐉 Monster Presets

### `characters/monster/castle_room1.json`
```json
{
    "_mode": "castle",
    "_name": "ปราสาท ห้อง 1",
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
    "_name": "ปราสาท ห้อง 2",
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
    "Weapon_Set": 3,           // 0-4 (ดูตาราง Weapon Sets)
    "Formation": 42.00,        // % Formation bonus
    "ATK_CHAR": 4488.00,       // ค่า ATK ที่แสดงในเกม
    "CRIT_DMG": 288.00,        // % Crit Damage
    "DMG_AMP_BUFF": 0.00,      // % DMG AMP (จากแหวน/buff)
    "ATK_PET": 391.00,         // ATK สัตว์เลี้ยง
    "BUFF_ATK_PET": 19.00,     // % BUFF ATK สัตว์เลี้ยง
    "Potential_PET": 0.00,     // % Potential สัตว์เลี้ยง
    "DEF_Target": 1461.00,     // DEF ของศัตรู
    "HP_Target": 17917.00,     // HP ของศัตรู
    "Target_HP_Percent": 30.00,// HP% เหลือ (for Lost HP Bonus)
    "DMG_Reduction": 10.00,    // % DMG Reduction ของศัตรู
    "DEF_BUFF": 0.00           // % DEF BUFF ของศัตรู
}
```

---

## 🎮 ATK_BASE Reference

| Rarity | Magic | Attack | Defense | Support | Balance |
|--------|-------|--------|---------|---------|---------|
| Legend | 1500 | 1500 | 727 | 1095 | 1306 |
| Rare | 1389 | 1389 | 704 | 1035 | 1238 |

**Implementation:** `constants.py` → `ATK_BASE` dict และ `get_atk_base()`

---

## 🐛 Lessons Learned / Gotchas (บทเรียนสำคัญ)

### 1. Weakness Damage = Base 30% + WEAK_DMG
> ⚠️ **สำคัญมาก!** เมื่อติดจุดอ่อน ไม่ใช่แค่ +WEAK_DMG แต่ต้องบวกฐาน 30% ด้วย

```python
# ❌ ผิด
weak_bonus = WEAK_DMG  # เช่น 35%

# ✅ ถูก  
weak_bonus = 30 + WEAK_DMG  # 30% (base) + 35% = 65%
```

**บทเรียน:** ดาเมจในเกมเป็น `ดาเมจคริ × 1.65` (ไม่ใช่ ×1.35)

---

### 2. Multi-Hit: Final Damage คือ "ต่อ Hit" ไม่ใช่รวม
> ⚠️ **อย่าสับสน!** สูตรคำนวณได้ดาเมจ **ต่อ Hit** แล้วค่อยคูณ SKILL_HITS

```python
# ❌ ผิด - หาร hits ก่อน
final_per_hit = ROUNDDOWN(raw_dmg / eff_def) / skill_hits

# ✅ ถูก - ดาเมจต่อ hit แล้วค่อยคูณ
final_per_hit = ROUNDDOWN(raw_dmg / eff_def)
total_damage = final_per_hit × skill_hits
```

**บทเรียน:** เมื่อเทียบกับเกม (เช่น 2,688) → ต้องรู้ว่าเป็น "ต่อ hit" หรือ "รวมทั้งหมด"

---

### 3. DMG_Reduction อยู่ใน RAW_DMG ไม่ใช่ Final
> ⚠️ **DMG_Reduction ถูกลบใน RAW step** ไม่ใช่หลังหาร DEF

```python
# สูตรที่ถูกต้อง (ใน RAW_DMG)
raw_dmg = ... × (1 + (DMG_AMP_DEBUFF - DMG_Reduction)/100)

# ❌ ไม่ใช่แบบนี้
final = raw_dmg / eff_def × (1 - DMG_Reduction/100)
```

---

### 4. Config Merge: Additive Keys ต้องบวกกัน
> ⚠️ **ค่าจาก character + user ต้อง ADD** ไม่ใช่ overwrite

```python
# ตัวอย่าง: Miho passive WEAK_DMG=23, user config=35
final_WEAK_DMG = 23 + 35 = 58
```

**บทเรียน:** ถ้าผลลัพธ์ผิด → เช็คว่า merge ถูกต้องไหม

---

### 5. Windows Console Thai Encoding
> ⚠️ **Windows CMD ไม่รองรับ UTF-8 ภาษาไทย** ต้องเพิ่ม:

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
```

**Implementation:** `main.py` บรรทัด 9-11

---

### 6. การทดสอบ: ต้องรู้ค่าเป้าหมายจากเกม
> 📌 **ก่อนทดสอบ ต้องรู้:**
> - ดาเมจในเกม (เช่น 2,688)
> - เป็น **ต่อ hit** หรือ **รวม**
> - เป็น **คริ** หรือ **ติดจุดอ่อน**
> - **สกิลไหน** (บน/ล่าง)

**บทเรียน:** ผิดพลาดบ่อยสุดคือ ไม่รู้ว่าเกมแสดงค่าอะไร

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
| Sun Wukong | Fire | Balance | Castle Mode (คริขั้นต่ำ) | `logic/sun_wukong.py` |
| Teo | Dark | Attack | Bonus Crit DMG | - |
| Yeonhee | Dark | Magic | HP-Based | - |

---

## 🧠 AI Agent Instructions

### การเพิ่มตัวละครใหม่

1. **ดึงข้อมูลจาก GameWith** → ใช้ Enhanced values
2. **สร้างไฟล์ JSON** ใน `characters/`
3. **ตัดสินใจว่าต้องการ logic พิเศษไหม:**
   - มี HP Alteration? → สร้าง `logic/[name].py`
   - มี HP condition bonus? → เพิ่ม field ที่เหมาะสม
   - มี Bonus Crit DMG? → ใช้ mapping อัตโนมัติ
   - มี Lost HP Bonus? → สร้าง logic file
4. **ถ้ามี logic พิเศษ:**
   - สร้างไฟล์ใน `logic/`
   - เพิ่ม import และเรียกใช้ใน `main.py`

### การแก้ไขไฟล์ตามหน้าที่

| ต้องการ | แก้ไขไฟล์ |
|---------|----------|
| เพิ่ม/แก้ UI/Menu | `menu.py` |
| เพิ่ม/แก้การแสดงผล | `display.py` |
| เพิ่ม/แก้การโหลด config | `config_loader.py` |
| เพิ่ม/แก้สูตรคำนวณ | `damage_calc.py` |
| เพิ่ม/แก้ค่าคงที่ | `constants.py` |
| เพิ่ม logic พิเศษ | `logic/[name].py` |
| จัด flow การทำงาน | `main.py` |

### การทดสอบ
```bash
python main.py           # Interactive mode
```

---

## ⚠️ Important Notes

1. **ทุกค่าเป็น %** → ต้อง `/100` ในสูตร
2. **ROUNDDOWN** → ดาเมจปัดลงเสมอ
3. **Base Weakness = 30%** → เพิ่มจาก WEAK_DMG
4. **Decimal** → ใช้ Python Decimal เพื่อความแม่นยำ
5. **skill1 = Top, skill2 = Bottom** → ลำดับใน JSON
6. **Metadata keys ขึ้นต้นด้วย `_`** → ถูกแยกออกจาก config
7. **Comment keys ขึ้นต้นด้วย `//`** → ถูกกรองออก

---

## 🔗 Data Source

- **Primary:** [GameWith - Seven Knights Rebirth](https://gamewith.net/sevenknights-rebirth/)
- **Values:** ใช้ **Enhanced** (ค่าสูงสุด) เสมอ
- **Transcend:** ระบุใน `_notes` ถ้ามีผลต่อค่า

---

## 📝 Changelog

### 2026-01-25: ATK Compare Mode
- เปลี่ยนโหมด 3 จาก "คำนวน ATK อย่างเดียว" เป็น **"เปรียบเทียบ ATK"**
- เพิ่มฟังก์ชัน `input_compare_values()` ใน `menu.py`
- เพิ่มฟังก์ชัน `select_atk_base()` สำหรับเลือก ATK_BASE (Legend/Rare/Custom)
- แสดงผลเปรียบเทียบระหว่าง config.json กับค่าที่กรอกใหม่

### 2026-01-24: Type Hints Refactor
- เพิ่ม type hints ครบทุกไฟล์ (100% coverage)
- ใช้ `from __future__ import annotations` สำหรับ modern syntax
- เพิ่ม `NumericType` type alias ใน `damage_calc.py`
- อัพเดท Python requirement เป็น 3.10+

### 2026-01-20: Sun Wukong Castle Mode
- เพิ่ม `logic/sun_wukong.py` - Castle Mode calculator
  - คำนวณว่าต้องติดคริขั้นต่ำกี่ครั้งถึงมอนจะตาย
  - สมมติทุก hit ติดจุดอ่อน บาง hit ติดคริเพิ่ม
- เพิ่ม `Weapon_Set = 4` ไฮดร้าตีปราสาท (DMG_AMP +30%)
- อัพเดท AGENTS.md

### 2026-01-12: Major Refactor
- แยก `main.py` (720 บรรทัด → ~300 บรรทัด) ออกเป็น:
  - `config_loader.py` - โหลด/merge config
  - `menu.py` - UI selection
  - `display.py` - output functions
- เพิ่ม monster presets สำหรับโหมดตีปราสาท
- ปรับปรุง AGENTS.md ให้ครบถ้วน

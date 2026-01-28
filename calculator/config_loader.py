"""
Config Loader - โหลดและจัดการ config files
"""

import json
from pathlib import Path
from decimal import Decimal
from typing import Any


def list_characters() -> list[str]:
    """แสดงรายชื่อตัวละครที่มี config"""
    chars_dir = Path(__file__).parent / "characters"
    if not chars_dir.exists():
        return []
    return [f.stem for f in chars_dir.glob("*.json")]


def load_json(path: Path) -> dict[str, Any]:
    """โหลด JSON และกรองค่า comment/metadata ออก"""
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                k: v for k, v in data.items() if not k.startswith("//") and not k.startswith("_")
            }
    return {}


def load_character_full(name: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """โหลด config จาก characters/[name].json รวม metadata"""
    char_path = Path(__file__).parent / "characters" / f"{name}.json"
    if char_path.exists():
        with open(char_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # แยก metadata และ config
            meta = {k: v for k, v in data.items() if k.startswith("_")}
            config = {k: v for k, v in data.items() 
                      if not k.startswith("//") and not k.startswith("_")}
            return meta, config
    return {}, {}


def load_user_config() -> dict[str, Any]:
    """โหลด config จาก config.json"""
    config_path = Path(__file__).parent / "config.json"
    return load_json(config_path)


def load_monster_preset(filename: str) -> dict[str, Any]:
    """โหลด monster preset จากไฟล์"""
    monster_dir = Path(__file__).parent / "characters" / "monster"
    monster_path = monster_dir / filename
    
    if monster_path.exists():
        with open(monster_path, "r", encoding="utf-8") as f:
            preset = json.load(f)
        # กรองเฉพาะค่าที่ไม่ใช่ null และไม่ขึ้นต้นด้วย _
        return {k: v for k, v in preset.items() if v is not None and not k.startswith("_")}
    return {}


def apply_weapon_set(config: dict[str, Any]) -> dict[str, Any]:
    """
    ใช้ชุดเซ็ทอาวุธตาม Weapon_Set
    0 = ไม่ใส่, 1 = จุดอ่อน(+35 WEAK), 2 = คริ(+15 IgnoreDEF), 
    3 = ไฮดร้า(+70 DMG_AMP), 4 = ตีปราสาท(+30 DMG_AMP)
    """
    weapon_set = int(config.get("Weapon_Set", 0))
    
    if weapon_set == 1:
        # จุดอ่อน: +35% WEAK_DMG
        config["WEAK_DMG"] = float(config.get("WEAK_DMG", 0)) + 35.0
    elif weapon_set == 2:
        # คริ: +15% Ignore_DEF
        config["Ignore_DEF"] = float(config.get("Ignore_DEF", 0)) + 15.0
    elif weapon_set == 3:
        # ไฮดร้า: +70% DMG_AMP_BUFF
        config["DMG_AMP_BUFF"] = float(config.get("DMG_AMP_BUFF", 0)) + 70.0
    elif weapon_set == 4:
        # ตีปราสาท: +30% DMG_AMP_BUFF
        config["DMG_AMP_BUFF"] = float(config.get("DMG_AMP_BUFF", 0)) + 30.0
    
    return config


def merge_configs(char_config: dict[str, Any], user_config: dict[str, Any]) -> dict[str, Any]:
    """
    รวม config โดย ADD ค่าที่เป็น % เข้าด้วยกัน
    - character: ค่าตายตัวจากตัวละคร
    - user: ค่าที่ผู้ใช้กรอก
    """
    merged = user_config.copy()
    
    # ค่าที่ต้อง ADD กัน (ทั้งสองฝ่ายอาจมีค่า)
    additive_keys = [
        "SKILL_DMG", "CRIT_DMG", "WEAK_DMG", "DMG_AMP_BUFF", "DMG_AMP_DEBUFF", 
        "DEF_REDUCE", "BUFF_ATK", "DMG_Reduction", "Ignore_DEF",
        "Bonus_DMG_HP_Target", "Cap_ATK_Percent"
    ]
    
    # ค่าที่ต้อง mapping ไปใส่ key อื่น (เช่น Bonus_Crit_DMG -> CRIT_DMG)
    mapping_keys: dict[str, str] = {
        "Bonus_Crit_DMG": "CRIT_DMG"
    }
    
    for key, value in char_config.items():
        if key in additive_keys:
            # ADD ค่าเข้าด้วยกัน
            user_value = user_config.get(key, 0)
            merged[key] = float(value) + float(user_value)
        elif key in mapping_keys:
            # Mapping key: ADD ไปใส่ key ปลายทาง
            target_key = mapping_keys[key]
            current_value = merged.get(target_key, 0)
            merged[target_key] = float(current_value) + float(value)
        elif key not in merged:
            # ค่าที่มีเฉพาะใน character (ใช้ค่า character)
            merged[key] = value
    
    return merged


def get_decimal(config: dict[str, Any], key: str, default: str = "0") -> Decimal:
    """ดึงค่าจาก config เป็น Decimal"""
    return Decimal(str(config.get(key, default)))

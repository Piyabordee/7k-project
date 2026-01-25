"""
Menu - UI/Menu selection functions
"""

from __future__ import annotations

from typing import Any
from config_loader import list_characters, load_character_full, load_monster_preset
from decimal import Decimal


def select_mode() -> tuple[str, dict[str, Any]]:
    """ให้ผู้ใช้เลือกโหมด (ปกติ / ตีปราสาท)"""
    print("\n--- เลือกโหมด (Select Mode) ---")
    print("  1. ปกติ (ใช้ค่าจาก config.json)")
    print("  2. ตีปราสาท")
    print("  3. คำนวน ATK")
    
    choice = input("\nเลือก [1-3]: ").strip()
    
    if choice == "3":
        print(">>> โหมด: เปรียบเทียบ ATK")
        return "atk_compare", {}
    elif choice == "2":
        # ถามเลือกห้อง
        print("\n--- เลือกห้อง (Select Room) ---")
        print("  1. ห้อง 1 (DEF=689, HP=8,650)")
        print("  2. ห้อง 2 (DEF=784, HP=10,790)")
        
        room_choice = input("\nเลือก [1-2]: ").strip()
        
        if room_choice == "2":
            monster_file = "castle_room2.json"
            print(">>> โหมด: ตีปราสาท ห้อง 2")
        else:
            monster_file = "castle_room1.json"
            print(">>> โหมด: ตีปราสาท ห้อง 1")
        
        return "castle", load_monster_preset(monster_file)
    else:
        print(">>> โหมด: ปกติ (ใช้ค่าจาก config.json)")
        return "normal", {}


def select_character() -> tuple[str | None, dict[str, Any], dict[str, Any]]:
    """ให้ผู้ใช้เลือกตัวละคร"""
    characters = list_characters()
    
    print("\n--- เลือกตัวละคร (Select Character) ---")
    
    for i, char in enumerate(characters, 1):
        print(f"  {i}. {char.capitalize()}")
    
    if not characters:
        print("  (ไม่พบไฟล์ตัวละคร)")
        return None, {}, {}
    
    choice = input(f"\nเลือก [1-{len(characters)}]: ").strip()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(characters):
            char_name = characters[idx]
            meta, config = load_character_full(char_name)
            return char_name, meta, config
    except ValueError:
        pass
    
    # Default to first character
    if characters:
        char_name = characters[0]
        meta, config = load_character_full(char_name)
        return char_name, meta, config
    
    return None, {}, {}


def select_skill(meta: dict[str, Any]) -> tuple[dict[str, Any], bool, list[dict[str, Any]] | None]:
    """
    ให้ผู้ใช้เลือกสกิล (ถ้ามีหลายสกิล)
    Returns: (skill_config, is_both_skills, all_skills_data)
    """
    skills = meta.get("_skills")
    
    if not skills:
        return {}, False, None
    
    print("\n--- เลือกสกิล (Select Skill) ---")
    skill_keys = list(skills.keys())
    
    for i, key in enumerate(skill_keys, 1):
        skill_data = skills[key]
        name = skill_data.get("_name", key)
        print(f"  {i}. {name}")
    
    # เพิ่มตัวเลือกทั้งสองสกิล
    if len(skill_keys) >= 2:
        print(f"  {len(skill_keys) + 1}. ทั้งสองสกิล")
    
    choice = input(f"\nเลือก [1-{len(skill_keys) + 1}]: ").strip()
    
    try:
        idx = int(choice) - 1
        
        # เลือกทั้งสองสกิล
        if idx == len(skill_keys) and len(skill_keys) >= 2:
            print(f">>> สกิล: ทั้งสองสกิล")
            # รวม config ของทุกสกิล (เอาสกิลแรกเป็นหลัก, สกิลอื่นใส่ใน all_skills)
            first_key = skill_keys[0]
            skill_config = skills[first_key].copy()
            skill_config = {k: v for k, v in skill_config.items() if not k.startswith("_")}
            
            # เก็บข้อมูลทุกสกิลสำหรับคำนวณรวม
            all_skills_data = []
            for key in skill_keys:
                skill_data = skills[key].copy()
                skill_name = skill_data.get("_name", key)
                skill_data = {k: v for k, v in skill_data.items() if not k.startswith("_")}
                all_skills_data.append({"name": skill_name, "config": skill_data})
            
            return skill_config, True, all_skills_data
        
        # เลือกสกิลเดียว
        if 0 <= idx < len(skill_keys):
            selected_key = skill_keys[idx]
            skill_config = skills[selected_key].copy()
            skill_config = {k: v for k, v in skill_config.items() if not k.startswith("_")}
            print(f">>> สกิล: {skills[selected_key].get('_name', selected_key)}")
            return skill_config, False, None
    except ValueError:
        pass
    
    # Default to first skill
    selected_key = skill_keys[0]
    skill_config = skills[selected_key].copy()
    skill_config = {k: v for k, v in skill_config.items() if not k.startswith("_")}
    print(f">>> สกิล: {skills[selected_key].get('_name', selected_key)}")
    return skill_config, False, None


def select_atk_base() -> tuple[Decimal, str]:
    """
    ให้ผู้ใช้เลือกค่า ATK_BASE
    Returns: (atk_base_value, description)
    """
    from constants import ATK_BASE
    
    print("\n--- เลือกค่าพลังโจมตีพื้นฐาน (Select Base ATK) ---")
    
    options = []
    
    # Legend
    for char_class, value in ATK_BASE["legend"].items():
        desc = f"Legend {char_class.capitalize()}: {value}"
        options.append((value, desc))
        
    # Rare
    for char_class, value in ATK_BASE["rare"].items():
        desc = f"Rare {char_class.capitalize()}: {value}"
        options.append((value, desc))
        
    # Custom
    options.append((None, "กำหนดเอง (Custom)"))
        
    for i, (_, desc) in enumerate(options, 1):
        print(f"  {i}. {desc}")
        
    choice = input(f"\nเลือก [1-{len(options)}]: ").strip()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            value, desc = options[idx]
            
            if value is None:
                # Custom input
                custom_val = input("ระบุค่า ATK_BASE: ").strip()
                return Decimal(custom_val), f"Custom ({custom_val})"
            
            return value, desc
    except (ValueError, IndexError):
        pass
        
    # Default
    print(">>> Invalid selection, using default (Legend Magic: 1500)")
    return Decimal("1500"), "Legend Magic (Default)"


def input_compare_values(config_values: dict[str, Decimal]) -> dict[str, Decimal]:
    """
    ให้ผู้ใช้กรอกค่าเปรียบเทียบ 2 อย่าง (Formation, ATK_CHAR)
    Returns: dict ของค่าที่ผู้ใช้กรอก
    """
    print("\n--- กรอกค่าเปรียบเทียบ (Input Compare Values) ---")
    print(f"ค่าปัจจุบันจาก config.json:")
    print(f"  Formation: {config_values['Formation']}%")
    print(f"  ATK_CHAR: {config_values['ATK_CHAR']}")
    print("\n(กด Enter เพื่อใช้ค่าเดิม)")
    
    compare_values = {}
    
    # Formation
    formation_input = input(f"Formation ใหม่ [{config_values['Formation']}]: ").strip()
    if formation_input:
        compare_values["Formation"] = Decimal(formation_input)
    else:
        compare_values["Formation"] = config_values["Formation"]
    
    # ATK_CHAR
    atk_char_input = input(f"ATK_CHAR ใหม่ [{config_values['ATK_CHAR']}]: ").strip()
    if atk_char_input:
        compare_values["ATK_CHAR"] = Decimal(atk_char_input)
    else:
        compare_values["ATK_CHAR"] = config_values["ATK_CHAR"]
    
    return compare_values

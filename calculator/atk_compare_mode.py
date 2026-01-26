from __future__ import annotations

from decimal import Decimal
from typing import Any

from constants import ATK_BASE
from damage_calc import calculate_total_atk
from config_loader import load_user_config, get_decimal
from display import print_calculation_header


def select_atk_base() -> tuple[Decimal, str]:
    """
    ให้ผู้ใช้เลือกค่า ATK_BASE
    Returns: (atk_base_value, description)
    """
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


def run_atk_compare_mode():
    """
    Runs the ATK Comparison mode logic
    """
    # โหลด user config มาเป็นค่าฐาน
    user_config = load_user_config()
    
    # ดึงค่าปัจจุบันจาก config
    current_values = {
        "Formation": get_decimal(user_config, "Formation", "0"),
        "ATK_CHAR": get_decimal(user_config, "ATK_CHAR", "4000"),
    }
    
    # ค่าพื้นฐานอื่นๆ (ไม่เปลี่ยน)
    atk_pet = get_decimal(user_config, "ATK_PET", "371")
    potential_pet = get_decimal(user_config, "Potential_PET", "21")
    buff_atk = get_decimal(user_config, "BUFF_ATK", "0")
    buff_atk_pet = get_decimal(user_config, "BUFF_ATK_PET", "17")
    
    # เลือก ATK_BASE
    atk_base, atk_base_desc = select_atk_base()
    
    # รับค่าเปรียบเทียบจากผู้ใช้
    compare_values = input_compare_values(current_values)
    
    print_calculation_header()
    
    # คำนวณ Total ATK - ค่าปัจจุบัน (จาก config)
    total_atk_current = calculate_total_atk(
        current_values["ATK_CHAR"], atk_pet, atk_base,
        current_values["Formation"], potential_pet,
        buff_atk, buff_atk_pet
    )
    
    # คำนวณ Total ATK - ค่าเปรียบเทียบ (จากผู้ใช้)
    total_atk_compare = calculate_total_atk(
        compare_values["ATK_CHAR"], atk_pet, atk_base,
        compare_values["Formation"], potential_pet,
        buff_atk, buff_atk_pet
    )
    
    # คำนวณส่วนต่าง
    atk_diff = total_atk_compare - total_atk_current
    
    # แสดงผลเปรียบเทียบ
    print("\n=== ค่าปัจจุบัน (config.json) ===")
    print(f"  Formation: {current_values['Formation']}%")
    print(f"  ATK_CHAR: {current_values['ATK_CHAR']}")
    print(f"  ATK_BASE: {atk_base} ({atk_base_desc})")
    print(f"  >>> Total ATK: {total_atk_current:.2f}")
    
    print("\n=== ค่าเปรียบเทียบ (กรอกใหม่) ===")
    print(f"  Formation: {compare_values['Formation']}%")
    print(f"  ATK_CHAR: {compare_values['ATK_CHAR']}")
    print(f"  ATK_BASE: {atk_base} ({atk_base_desc})")
    print(f"  >>> Total ATK: {total_atk_compare:.2f}")
    
    print("\n" + "=" * 50)
    print("=== ผลเปรียบเทียบ ===")
    print("=" * 50)
    
    # แสดงส่วนต่าง ATK
    if atk_diff > 0:
        print(f"  ✅ ค่าใหม่ แซง +{atk_diff:.2f} ATK")
    elif atk_diff < 0:
        print(f"  ❌ ค่าปัจจุบัน เหนือกว่า +{abs(atk_diff):.2f} ATK")
    else:
        print(f"  ➡️ ATK เท่ากัน")

"""
Display - ฟังก์ชันแสดงผลทั้งหมด
"""

from decimal import Decimal
from typing import Any
from damage_calc import (
    calculate_total_atk,
    calculate_dmg_hp,
    calculate_cap_atk,
    calculate_final_dmg_hp,
    calculate_raw_dmg,
    calculate_effective_def,
    calculate_final_dmg,
)
from config_loader import merge_configs


def print_header() -> None:
    """แสดง header ของโปรแกรม"""
    print("=" * 60)
    print("  7k Rebirth - Damage Calculator")
    print("=" * 60)


def print_character_info(char_name: str, rarity: str, char_class: str, atk_base: int | Decimal) -> None:
    """แสดงข้อมูลตัวละคร"""
    if char_name:
        print(f"\n>>> ตัวละคร: {char_name.capitalize()} ({rarity} {char_class})")
        print(f">>> ATK_BASE = {atk_base}")


def print_weapon_set(weapon_set: int):
    """แสดงข้อมูลชุดเซ็ทอาวุธ"""
    weapon_names = {
        0: "ไม่ใส่", 
        1: "จุดอ่อน (+35% WEAK)", 
        2: "คริ (+15% Ignore DEF)", 
        3: "ไฮดร้า (+70% DMG_AMP)",
        4: "ตีปราสาท (+30% DMG_AMP)"
    }
    print(f">>> โหลด config.json (ชุดเซ็ทอาวุธ: {weapon_names.get(weapon_set, 'ไม่ทราบ')})")


def print_input_values(
    atk_char: Decimal, atk_pet: Decimal, formation: Decimal, potential_pet: Decimal,
    buff_atk: Decimal, buff_atk_pet: Decimal, skill_dmg: Decimal, skill_hits: int,
    crit_dmg: Decimal, weak_dmg: Decimal, dmg_amp_buff: Decimal, dmg_amp_debuff: Decimal,
    def_target: Decimal, def_reduce: Decimal, ignore_def: Decimal,
    char_config: dict[str, Any], user_config: dict[str, Any]
) -> None:
    """แสดงค่า Input (Character + User)"""
    print("\n--- Input Values (Character + User) ---")
    print(f"ATK_CHAR: {atk_char:,.0f}  |  ATK_PET: {atk_pet:,.0f}")
    print(f"Formation: {formation}%  |  Potential_PET: {potential_pet}%")
    print(f"BUFF_ATK: {buff_atk}%  |  BUFF_ATK_PET: {buff_atk_pet}%")
    
    if char_config.get("SKILL_DMG"):
        if skill_hits > 1:
            print(f"\nSKILL_DMG: {skill_dmg}% x {skill_hits} hits = {skill_dmg * skill_hits}%")
        else:
            print(f"\nSKILL_DMG: {skill_dmg}% (char: {char_config.get('SKILL_DMG', 0)})")
    else:
        print(f"\nSKILL_DMG: {skill_dmg}%")
    
    print(f"CRIT_DMG: {crit_dmg}%")
    
    char_weak = char_config.get("WEAK_DMG", 0)
    user_weak = user_config.get("WEAK_DMG", 0)
    if char_weak:
        print(f"WEAK_DMG: {weak_dmg}% (char: {char_weak} + user: {user_weak})")
    else:
        print(f"WEAK_DMG: {weak_dmg}%")
    
    char_amp_buff = char_config.get("DMG_AMP_BUFF", 0)
    user_amp_buff = user_config.get("DMG_AMP_BUFF", 0)
    if char_amp_buff or user_amp_buff:
        print(f"DMG_AMP_BUFF: {dmg_amp_buff}% (char: {char_amp_buff} + user: {user_amp_buff})")
    
    char_amp_debuff = char_config.get("DMG_AMP_DEBUFF", 0)
    user_amp_debuff = user_config.get("DMG_AMP_DEBUFF", 0)
    if char_amp_debuff or user_amp_debuff:
        print(f"DMG_AMP_DEBUFF: {dmg_amp_debuff}% (char: {char_amp_debuff} + user: {user_amp_debuff})")
    
    print(f"\nDEF_Target: {def_target:,.0f}")
    
    char_def_reduce = char_config.get("DEF_REDUCE", 0)
    user_def_reduce = user_config.get("DEF_REDUCE", 0)
    if char_def_reduce:
        print(f"DEF_REDUCE: {def_reduce}% (char: {char_def_reduce} + user: {user_def_reduce})")
    else:
        print(f"DEF_REDUCE: {def_reduce}%")
    
    print(f"Ignore_DEF: {ignore_def}%")


def print_calculation_header() -> None:
    """แสดง header ผลการคำนวณ"""
    print("\n" + "=" * 60)
    print("  ผลการคำนวณ (Calculation Results)")
    print("=" * 60)


def print_total_atk(total_atk: Decimal) -> None:
    """แสดง Total ATK"""
    print(f"\n1. Total_ATK = {total_atk:,.2f}")


def print_hp_based_damage(dmg_hp: Decimal, cap_atk: Decimal, final_dmg_hp: Decimal) -> None:
    """แสดง HP-Based Damage"""
    if dmg_hp > 0:
        print(f"2. DMG_HP = {dmg_hp:,.2f}")
        print(f"   Cap_ATK = {cap_atk:,.2f}")
        print(f"   Final_DMG_HP = {final_dmg_hp:,.0f}")
    else:
        print(f"2. HP-Based Damage = 0 (ไม่ใช้)")


def print_raw_damage(raw_dmg_crit: Decimal, raw_dmg_crit_weakness: Decimal) -> None:
    """แสดง RAW Damage"""
    print(f"\n3. RAW_DMG (คริ) = {raw_dmg_crit:,.2f}")
    print(f"   RAW_DMG (คริ+จุดอ่อน) = {raw_dmg_crit_weakness:,.2f}")


def print_effective_def(effective_def: Decimal) -> None:
    """แสดง Effective DEF"""
    print(f"4. Effective_DEF = {effective_def:.2f}")


def calc_atk_needed(current_dmg: int, monster_hp: int, current_atk: Decimal) -> int:
    """คำนวณว่าต้องเพิ่ม ATK_CHAR อีกเท่าไหร่ถึงจะฆ่ามอนได้"""
    if current_dmg <= 0 or monster_hp <= 0:
        return 0
    remaining = monster_hp - current_dmg
    if remaining <= 0:
        return 0  # ฆ่าได้แล้ว ไม่ต้องเพิ่ม
    atk_needed = float(current_atk) * (remaining / current_dmg)
    return int(atk_needed) + 1  # ปัดขึ้น


def print_kill_status_block(hp_target: Decimal, dmg_1: Decimal, label_1: str, dmg_2: Decimal, label_2: str) -> None:
    """แสดงสถานะการฆ่ามอนสเตอร์ (Overkill / Remaining)"""
    hp_int = int(hp_target)
    
    print("\n" + "-" * 60)
    print(f"  🐉 HP มอนสเตอร์: {hp_int:,}")
    print("-" * 60)
    
    # Check 1
    if int(dmg_1) >= hp_int:
        overkill = int(dmg_1) - hp_int
        print(f"  💀 [{label_1}] มอนตาย! (เกิน {overkill:,})")
    else:
        remaining_hp = hp_int - int(dmg_1)
        remaining_percent = (remaining_hp / hp_int) * 100
        print(f"  ❌ [{label_1}] มอนไม่ตาย ขาด {remaining_percent:.1f}% ({remaining_hp:,})")
    
    # Check 2
    if int(dmg_2) >= hp_int:
        overkill = int(dmg_2) - hp_int
        print(f"  💀 [{label_2}] มอนตาย! (เกิน {overkill:,})")
    else:
        remaining_hp = hp_int - int(dmg_2)
        remaining_percent = (remaining_hp / hp_int) * 100
        print(f"  ❌ [{label_2}] มอนไม่ตาย ขาด {remaining_percent:.1f}% ({remaining_hp:,})")
    
    print("-" * 60)


def get_hp_status(damage: int, monster_hp: int, current_atk: Decimal) -> str:
    """สร้างข้อความเลือดมอน"""
    if monster_hp <= 0:
        return ""  # ไม่ใช่โหมดปราสาท
    remaining = int(monster_hp) - damage
    if remaining <= 0:
        return f" 💀 มอนตาย (เกิน {-remaining:,})"
    else:
        return f" ❤️ เหลือเลือด {remaining:,}"


def print_final_damage_results(
    skill_hits: int, weak_dmg: Decimal,
    final_dmg_crit: int, final_dmg_crit_weakness: int,
    final_dmg_no_crit: int, final_dmg_weakness_only: int,
    monster_hp: int, atk_char: Decimal
) -> None:
    """แสดงผล Final Damage Results"""
    print("\n" + "-" * 40)
    print("  Final Damage Results")
    print("-" * 40)
    
    if skill_hits > 1:
        total_crit = final_dmg_crit * skill_hits
        total_crit_weakness = final_dmg_crit_weakness * skill_hits
        total_no_crit = final_dmg_no_crit * skill_hits
        total_weakness_only = final_dmg_weakness_only * skill_hits
        
        print(f"  ติดคริ: {total_crit:,} ({skill_hits} hits x {final_dmg_crit:,}/hit){get_hp_status(total_crit, monster_hp, atk_char)}")
        print(f"  ติดคริ+จุดอ่อน: {total_crit_weakness:,} (+{weak_dmg}%) ({skill_hits} hits x {final_dmg_crit_weakness:,}/hit){get_hp_status(total_crit_weakness, monster_hp, atk_char)}")
        print(f"  ไม่ติดคริ: {total_no_crit:,} ({skill_hits} hits x {final_dmg_no_crit:,}/hit){get_hp_status(total_no_crit, monster_hp, atk_char)}")
        print(f"  ติดแค่จุดอ่อน: {total_weakness_only:,} (+{weak_dmg}%) ({skill_hits} hits x {final_dmg_weakness_only:,}/hit){get_hp_status(total_weakness_only, monster_hp, atk_char)}")
    else:
        total_crit = final_dmg_crit
        total_crit_weakness = final_dmg_crit_weakness
        total_no_crit = final_dmg_no_crit
        total_weakness_only = final_dmg_weakness_only
        print(f"  ติดคริ: {final_dmg_crit:,}{get_hp_status(total_crit, monster_hp, atk_char)}")
        print(f"  ติดคริ+จุดอ่อน: {final_dmg_crit_weakness:,} (+{weak_dmg}%){get_hp_status(total_crit_weakness, monster_hp, atk_char)}")
        print(f"  ไม่ติดคริ: {final_dmg_no_crit:,}{get_hp_status(total_no_crit, monster_hp, atk_char)}")
        print(f"  ติดแค่จุดอ่อน: {final_dmg_weakness_only:,} (+{weak_dmg}%){get_hp_status(total_weakness_only, monster_hp, atk_char)}")
    
    print("-" * 40)


def print_espada_results(espada_result: dict[str, Any], weak_dmg: Decimal, final_dmg_hp: Decimal) -> None:
    """แสดงผล Espada แบบพิเศษ"""
    print("\n" + "=" * 60)
    print("  Espada Special Calculation (4 กรณี)")
    print("=" * 60)
    
    print(f"\n[1] คริ (ไม่มี HP-based):")
    print(f"    RAW_DMG = {espada_result['crit_no_hp']['raw']:,.2f}")
    print(f"    Final = {espada_result['crit_no_hp']['final']:,}")
    
    print(f"\n[2] คริ + HP-based (HP: {final_dmg_hp:,}):")
    print(f"    RAW_DMG = {espada_result['crit_with_hp']['raw']:,.2f}")
    print(f"    Final = {espada_result['crit_with_hp']['final']:,}")
    
    print(f"\n[3] จุดอ่อน (+{weak_dmg}%) (ไม่มี HP-based):")
    print(f"    RAW_DMG = {espada_result['weak_no_hp']['raw']:,.2f}")
    print(f"    Final = {espada_result['weak_no_hp']['final']:,}")
    
    print(f"\n[4] จุดอ่อน (+{weak_dmg}%) + HP-based:")
    print(f"    RAW_DMG = {espada_result['weak_with_hp']['raw']:,.2f}")
    print(f"    Final = {espada_result['weak_with_hp']['final']:,}")
    
    print("\n" + "=" * 60)
    print(f">>> ดาเมจสูงสุด (คริ+HP): {espada_result['crit_with_hp']['final']:,} <<<")
    print(f">>> ดาเมจสูงสุด (จุดอ่อน+HP): {espada_result['weak_with_hp']['final']:,} <<<")
    print("=" * 60)


def print_both_skills_results(
    all_skills_data: list[dict[str, Any]], char_config: dict[str, Any], user_config: dict[str, Any], 
    total_atk: Decimal, crit_dmg: Decimal, weak_dmg: Decimal, 
    dmg_amp_buff: Decimal, dmg_amp_debuff: Decimal, dmg_reduction: Decimal,
    def_target: Decimal, def_buff: Decimal, def_reduce: Decimal, hp_target: Decimal
) -> None:
    """แสดงผลรวมทั้งสองสกิล"""
    print("\n" + "=" * 60)
    print("  📊 รวมทั้งสองสกิล (Both Skills)")
    print("=" * 60)
    
    # คำนวณดาเมจแต่ละสกิล
    total_damage_crit = Decimal("0")
    total_damage_weak = Decimal("0")
    
    for skill_info in all_skills_data:
        skill_name = skill_info["name"]
        s_config = skill_info["config"]
        
        # Merge skill config with user config
        merged_skill_config = char_config.copy()
        merged_skill_config.update(s_config)
        merged_skill = merge_configs(merged_skill_config, user_config)
        
        s_skill_dmg = Decimal(str(merged_skill.get("SKILL_DMG", 0)))
        s_skill_hits = int(merged_skill.get("SKILL_HITS", 1))
        s_ignore_def = Decimal(str(merged_skill.get("Ignore_DEF", 0)))
        s_hp_alteration = Decimal(str(merged_skill.get("HP_Alteration", 0)))
        s_bonus_hp = Decimal(str(merged_skill.get("Bonus_DMG_HP_Target", 0)))
        s_cap_atk = Decimal(str(merged_skill.get("Cap_ATK_Percent", 0)))
        
        # คำนวณ Effective DEF สำหรับสกิลนี้
        s_eff_def = calculate_effective_def(def_target, def_buff, def_reduce, s_ignore_def)
        
        # HP-based damage
        s_dmg_hp = calculate_dmg_hp(hp_target, s_bonus_hp)
        s_cap = calculate_cap_atk(total_atk, s_cap_atk)
        s_final_hp = calculate_final_dmg_hp(s_dmg_hp, s_cap)
        
        # HP Alteration (Freyja)
        s_hp_alt_dmg = Decimal("0")
        if s_hp_alteration > 0:
            s_hp_alt_dmg = hp_target * (Decimal("100") - s_hp_alteration) / Decimal("100")
        
        # RAW damage
        s_raw_crit = calculate_raw_dmg(
            total_atk, s_skill_dmg, crit_dmg, Decimal("0"),
            dmg_amp_buff, dmg_amp_debuff, dmg_reduction, s_final_hp
        )
        s_raw_weak = calculate_raw_dmg(
            total_atk, s_skill_dmg, crit_dmg, Decimal("30") + weak_dmg,
            dmg_amp_buff, dmg_amp_debuff, dmg_reduction, s_final_hp
        )
        
        # Final damage per skill
        s_final_crit = calculate_final_dmg(s_raw_crit, s_eff_def) * s_skill_hits + int(s_hp_alt_dmg)
        s_final_weak = calculate_final_dmg(s_raw_weak, s_eff_def) * s_skill_hits + int(s_hp_alt_dmg)
        
        total_damage_crit += s_final_crit
        total_damage_weak += s_final_weak
        
        print(f"\n  [{skill_name}]")
        print(f"    ดาเมจคริ: {s_final_crit:,}")
        print(f"    ดาเมจติดจุดอ่อน: {s_final_weak:,}")
    
    print("\n" + "-" * 60)
    print(f"  🎯 ดาเมจรวม (คริ): {int(total_damage_crit):,}")
    print(f"  🎯 ดาเมจรวม (จุดอ่อน): {int(total_damage_weak):,}")
    
    # เช็คว่ามอนตายไหม using reusable function
    print_kill_status_block(
        hp_target, 
        total_damage_crit, "คริ", 
        total_damage_weak, "จุดอ่อน"
    )
    
    print("=" * 60)

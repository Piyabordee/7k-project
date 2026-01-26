"""
7k Rebirth Damage Calculator - CLI Interface
Main Entry Point - ดึงทุก module มารัน
"""

import sys
import io

# Fix encoding for Windows console (Thai text support)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

from decimal import Decimal
from damage_calc import (
    calculate_total_atk,
    calculate_dmg_hp,
    calculate_cap_atk,
    calculate_final_dmg_hp,
    calculate_raw_dmg,
    calculate_effective_def,
    calculate_final_dmg,
)
from constants import get_atk_base
from config_loader import (
    load_user_config,
    apply_weapon_set,
    merge_configs,
    get_decimal,
)
from menu import select_mode, select_character, select_skill
from atk_compare_mode import run_atk_compare_mode
from display import (
    print_header,
    print_character_info,
    print_weapon_set,
    print_input_values,
    print_calculation_header,
    print_total_atk,
    print_hp_based_damage,
    print_raw_damage,
    print_effective_def,
    print_final_damage_results,
    print_espada_results,
    print_both_skills_results,
)


def main():
    print_header()
    
    # เลือกโหมด (ปกติ / ตีปราสาท / คำนวน ATK)
    mode, monster_preset = select_mode()
    
    if mode == "atk_compare":
        run_atk_compare_mode()
        return
    
    # เลือกตัวละคร
    char_name, char_meta, char_config = select_character()
    
    # ดึง ATK_BASE จาก rarity และ class
    rarity = char_meta.get("_rarity", "legend")
    char_class = char_meta.get("_class", "magic")
    atk_base = get_atk_base(rarity, char_class)
    
    print_character_info(char_name, rarity, char_class, atk_base)
    
    # เลือกสกิล (ถ้ามีหลายสกิล)
    skill_config, is_both_skills, all_skills_data = select_skill(char_meta)
    
    # โหลด user config
    user_config = load_user_config()
    
    # Override ด้วย monster preset (ถ้ามี)
    if monster_preset:
        user_config.update(monster_preset)
    
    # ใช้ชุดเซ็ทอาวุธ
    user_config = apply_weapon_set(user_config)
    weapon_set = int(user_config.get("Weapon_Set", 0))
    print_weapon_set(weapon_set)
    
    # รวม config: char + skill + user (ADD ค่าเข้าด้วยกัน)
    combined_char_config = char_config.copy()
    combined_char_config.update(skill_config)  # Skill overrides/adds to char
    config = merge_configs(combined_char_config, user_config)
    
    # ดึงค่าจาก config
    atk_char = get_decimal(config, "ATK_CHAR", "4000")
    buff_atk = get_decimal(config, "BUFF_ATK", "0")
    formation = get_decimal(config, "Formation", "21")
    atk_pet = get_decimal(config, "ATK_PET", "371")
    buff_atk_pet = get_decimal(config, "BUFF_ATK_PET", "17")
    potential_pet = get_decimal(config, "Potential_PET", "21")
    
    skill_dmg = get_decimal(config, "SKILL_DMG", "160")
    skill_hits = int(config.get("SKILL_HITS", 1))
    crit_dmg = get_decimal(config, "CRIT_DMG", "256")
    weak_dmg = get_decimal(config, "WEAK_DMG", "0")
    dmg_amp_buff = get_decimal(config, "DMG_AMP_BUFF", "0")
    dmg_amp_debuff = get_decimal(config, "DMG_AMP_DEBUFF", "0")
    dmg_reduction = get_decimal(config, "DMG_Reduction", "0")
    
    def_reduce = get_decimal(config, "DEF_REDUCE", "0")
    ignore_def = get_decimal(config, "Ignore_DEF", "39")
    def_target = get_decimal(config, "DEF_Target", "784")
    def_buff = get_decimal(config, "DEF_BUFF", "0")
    
    bonus_dmg_hp_target = get_decimal(config, "Bonus_DMG_HP_Target", "0")
    cap_atk_percent = get_decimal(config, "Cap_ATK_Percent", "0")
    hp_target = get_decimal(config, "HP_Target", "10790")
    
    # แสดงค่า Input
    print_input_values(
        atk_char, atk_pet, formation, potential_pet,
        buff_atk, buff_atk_pet, skill_dmg, skill_hits,
        crit_dmg, weak_dmg, dmg_amp_buff, dmg_amp_debuff,
        def_target, def_reduce, ignore_def,
        char_config, user_config
    )
    
    # === คำนวณ ===
    print_calculation_header()
    
    # 1. Total ATK
    total_atk = calculate_total_atk(
        atk_char, atk_pet, atk_base, 
        formation, potential_pet, 
        buff_atk, buff_atk_pet
    )
    print_total_atk(total_atk)
    
    # 2. HP-Based Damage
    dmg_hp = calculate_dmg_hp(hp_target, bonus_dmg_hp_target)
    cap_atk = calculate_cap_atk(total_atk, cap_atk_percent)
    final_dmg_hp = calculate_final_dmg_hp(dmg_hp, cap_atk)
    print_hp_based_damage(dmg_hp, cap_atk, final_dmg_hp)
    
    # 3. RAW Damage (แยกคำนวณ 4 แบบ)
    # 3.1 RAW คริ (ไม่ติดจุดอ่อน, WEAK_DMG = 0)
    raw_dmg_crit = calculate_raw_dmg(
        total_atk, skill_dmg, crit_dmg, Decimal("0"),
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, final_dmg_hp
    )
    
    # 3.2 RAW คริ+ติดจุดอ่อน (30% พื้นฐาน + WEAK_DMG จาก config)
    total_weak_dmg = Decimal("30") + weak_dmg
    raw_dmg_crit_weakness = calculate_raw_dmg(
        total_atk, skill_dmg, crit_dmg, total_weak_dmg,
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, final_dmg_hp
    )
    
    # 3.3 RAW ไม่คริ (CRIT_DMG = 100, WEAK_DMG = 0)
    raw_dmg_no_crit = calculate_raw_dmg(
        total_atk, skill_dmg, Decimal("100"), Decimal("0"),
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, final_dmg_hp
    )
    
    # 3.4 RAW ติดจุดอ่อนอย่างเดียว (CRIT_DMG = 100, WEAK_DMG = 30 + config)
    raw_dmg_weakness_only = calculate_raw_dmg(
        total_atk, skill_dmg, Decimal("100"), total_weak_dmg,
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, final_dmg_hp
    )
    
    print_raw_damage(raw_dmg_crit, raw_dmg_crit_weakness)
    
    # 4. Effective DEF
    effective_def = calculate_effective_def(def_target, def_buff, def_reduce, ignore_def)
    print_effective_def(effective_def)
    
    # ตรวจสอบว่ามี HP Alteration หรือไม่ (Freyja)
    hp_alteration = get_decimal(config, "HP_Alteration", "0")
    
    # ตรวจสอบว่าเป็น Freyja หรือไม่ (ใช้ logic พิเศษ - HP Alteration)
    if char_name and char_name.lower() == "freyja" and hp_alteration > 0 and not is_both_skills:
        from logic.freyja import calculate_freyja_damage, print_freyja_results
        
        freyja_result = calculate_freyja_damage(
            total_atk=total_atk,
            skill_dmg=skill_dmg,
            crit_dmg=crit_dmg,
            weak_dmg=weak_dmg,
            dmg_amp_buff=dmg_amp_buff,
            dmg_amp_debuff=dmg_amp_debuff,
            dmg_reduction=dmg_reduction,
            eff_def=effective_def,
            skill_hits=skill_hits,
            hp_target=hp_target,
            hp_alteration=hp_alteration
        )
        
        print_freyja_results(freyja_result, hp_target)
        return
    
    # ตรวจสอบว่าเป็น Ryan หรือไม่ (ใช้ logic พิเศษ - Lost HP Bonus)
    lost_hp_bonus = get_decimal(config, "Lost_HP_Bonus", "0")
    weak_skill_dmg = get_decimal(config, "WEAK_SKILL_DMG", "0")
    target_hp_percent = get_decimal(config, "Target_HP_Percent", "100")
    
    if char_name and char_name.lower() == "ryan" and lost_hp_bonus > 0 and not is_both_skills:
        from logic.ryan import calculate_ryan_damage, print_ryan_results
        
        ryan_result = calculate_ryan_damage(
            total_atk=total_atk,
            skill_dmg=skill_dmg,
            weak_skill_dmg=weak_skill_dmg,
            crit_dmg=crit_dmg,
            weak_dmg=weak_dmg,
            dmg_amp_buff=dmg_amp_buff,
            dmg_amp_debuff=dmg_amp_debuff,
            dmg_reduction=dmg_reduction,
            eff_def=effective_def,
            skill_hits=skill_hits,
            lost_hp_bonus=lost_hp_bonus,
            target_hp_percent=target_hp_percent
        )
        
        print_ryan_results(ryan_result)
        return
    
    # ตรวจสอบว่าเป็น Klahan หรือไม่ (ใช้ logic พิเศษ - HP condition bonus)
    hp_above_50_bonus = get_decimal(config, "HP_Above_50_Bonus", "0")
    hp_below_50_bonus = get_decimal(config, "HP_Below_50_Bonus", "0")
    
    if char_name and char_name.lower() == "klahan" and (hp_above_50_bonus > 0 or hp_below_50_bonus > 0) and not is_both_skills:
        from logic.klahan import calculate_klahan_damage, print_klahan_results
        
        # ดึงชื่อสกิลจาก skill_config
        skill_name_display = skill_config.get("_name", "Skill")
        if "_name" not in skill_config:
            # ถ้าไม่มีชื่อใน config ให้หาจาก char_meta
            skills = char_meta.get("_skills", {})
            for key, val in skills.items():
                if val.get("HP_Above_50_Bonus") == float(hp_above_50_bonus) or val.get("HP_Below_50_Bonus") == float(hp_below_50_bonus):
                    skill_name_display = val.get("_name", key)
                    break
        
        klahan_result = calculate_klahan_damage(
            total_atk=total_atk,
            skill_dmg=skill_dmg,
            hp_above_50_bonus=hp_above_50_bonus,
            hp_below_50_bonus=hp_below_50_bonus,
            crit_dmg=crit_dmg,
            weak_dmg=weak_dmg,
            dmg_amp_buff=dmg_amp_buff,
            dmg_amp_debuff=dmg_amp_debuff,
            dmg_reduction=dmg_reduction,
            eff_def=effective_def,
            skill_hits=skill_hits,
            skill_name=skill_name_display
        )
        
        print_klahan_results(klahan_result)
        return
    
    # ตรวจสอบว่าเป็น Sun Wukong + โหมดตีปราสาท (ใช้ Castle Mode logic)
    if char_name and char_name.lower() == "sun_wukong" and monster_preset and not is_both_skills:
        from logic.sun_wukong import calculate_sun_wukong_castle_mode, print_castle_mode_results
        
        # ดึงชื่อสกิลจาก skill_config
        skill_name_display = skill_config.get("_name", "Skill")
        if "_name" not in skill_config:
            skills = char_meta.get("_skills", {})
            for key, val in skills.items():
                if val.get("SKILL_DMG") == float(skill_dmg):
                    skill_name_display = val.get("_name", key)
                    break
        
        wukong_result = calculate_sun_wukong_castle_mode(
            total_atk=total_atk,
            skill_dmg=skill_dmg,
            crit_dmg=crit_dmg,
            weak_dmg=weak_dmg,
            dmg_amp_buff=dmg_amp_buff,
            dmg_amp_debuff=dmg_amp_debuff,
            dmg_reduction=dmg_reduction,
            eff_def=effective_def,
            skill_hits=skill_hits,
            hp_target=hp_target,
            skill_name=skill_name_display,
            final_dmg_hp=final_dmg_hp
        )
        
        print_castle_mode_results(wukong_result)
        return
    
    # ตรวจสอบว่าเป็น Espada หรือไม่ (ใช้ logic พิเศษ)
    if char_name and char_name.lower() == "espada" and bonus_dmg_hp_target > 0 and not is_both_skills:
        from logic.espada import calculate_espada_damage
        
        espada_result = calculate_espada_damage(
            total_atk, skill_dmg, crit_dmg, weak_dmg,
            dmg_amp_buff, dmg_amp_debuff, dmg_reduction,
            effective_def, hp_target, bonus_dmg_hp_target, cap_atk_percent
        )
        
        print_espada_results(espada_result, weak_dmg, final_dmg_hp)
        return

    # ตรวจสอบว่าเป็น Biscuit หรือไม่ (ใช้ logic พิเศษ - Dual Scaling ATK + DEF)
    if char_name and char_name.lower() == "biscuit":
        from logic.biscuit import calculate_biscuit_damage, print_biscuit_results
        
        # อ่านค่า DEF_CHAR, DEF_PET จาก config หรือถาม User
        print("\n--- Biscuit Special Stats Input ---")
        try:
            default_def_char = config.get("DEF_CHAR", "0")
            in_def_char = input(f"Enter DEF_CHAR (Default {default_def_char}): ").strip()
            def_char = Decimal(in_def_char) if in_def_char else Decimal(str(default_def_char))
            
            default_def_pet = config.get("DEF_PET", "0")
            in_def_pet = input(f"Enter DEF_PET (Default {default_def_pet}): ").strip()
            def_pet = Decimal(in_def_pet) if in_def_pet else Decimal(str(default_def_pet))
        except Exception as e:
            print(f"Input Error: {e}. Using config values.")
            def_char = get_decimal(config, "DEF_CHAR", "0")
            def_pet = get_decimal(config, "DEF_PET", "0")
        
        # Biscuit มี 2 parts: ATK scaling (SKILL_DMG) + DEF scaling (SKILL_DMG_fromDef)
        # เราต้องหาค่า SKILL_DMG ที่เป็น part ของ DEF
        # สมมติว่าใน config json เก็บแยก หรือถ้าไม่ได้แยก เราอาจต้อง hardcode หรือดึงจาก _notes?
        # User prompt indicates Biscuit config has "Skill 2: +135% DEF Scaling" in _notes
        # But wait, in the JSON we made:
        # "skill2": { "SKILL_DMG": 115.00, ... }
        # The DEF scaling (135%) wasn't in a specific field in the JSON structure I created, only in notes.
        # I need to EXTRACT it or rely on user adding it to config.
        # "SKILL_DMG_fromDef" is what logic.biscuit expects.
        # Let's check config for "SKILL_DMG_fromDef", default to 135 if skill is skill2 (Leap Attack).
        
        skill_dmg_from_def = get_decimal(config, "SKILL_DMG_DEF", "0")
        
        # Auto-detect check removed as user provided it in JSON
        if skill_dmg_from_def == 0 and "Leap Attack" in skill_config.get("_name", ""):
             # Fallback if not updated in json yet, but user just updated it.
             # Let's keep a fallback or just trust the config.
             # User said "Use this", so I rely on config.
             pass
        
        biscuit_result = calculate_biscuit_damage(
            total_atk=total_atk,
            skill_dmg_atk=skill_dmg,
            skill_dmg_def=skill_dmg_from_def,
            crit_dmg=crit_dmg,
            weak_dmg=weak_dmg,
            dmg_amp_buff=dmg_amp_buff,
            dmg_amp_debuff=dmg_amp_debuff,
            dmg_reduction=dmg_reduction,
            eff_def=effective_def,
            skill_hits=skill_hits,
            def_char=def_char,
            def_pet=def_pet,
            final_dmg_hp=final_dmg_hp
        )
        
        print_biscuit_results(biscuit_result)
        return
    
    # 5. Final Damage (ต่อ 1 hit) - สำหรับตัวละครปกติ
    final_dmg_crit = calculate_final_dmg(raw_dmg_crit, effective_def)
    final_dmg_crit_weakness = calculate_final_dmg(raw_dmg_crit_weakness, effective_def)
    final_dmg_no_crit = calculate_final_dmg(raw_dmg_no_crit, effective_def)
    final_dmg_weakness_only = calculate_final_dmg(raw_dmg_weakness_only, effective_def)
    
    # ดึง HP มอนจาก monster_preset (ถ้ามี)
    monster_hp = monster_preset.get("HP_Target", 0) if monster_preset else 0
    
    print_final_damage_results(
        skill_hits, weak_dmg,
        final_dmg_crit, final_dmg_crit_weakness,
        final_dmg_no_crit, final_dmg_weakness_only,
        monster_hp, atk_char
    )
    
    # === ถ้าเลือกทั้งสองสกิล: คำนวณดาเมจรวมและเช็คว่ามอนตายไหม ===
    if is_both_skills and all_skills_data:
        print_both_skills_results(
            all_skills_data, char_config, user_config,
            total_atk, crit_dmg, weak_dmg,
            dmg_amp_buff, dmg_amp_debuff, dmg_reduction,
            def_target, def_buff, def_reduce, hp_target
        )


if __name__ == "__main__":
    main()

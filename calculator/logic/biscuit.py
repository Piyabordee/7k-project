from decimal import Decimal
from damage_calc import calculate_raw_dmg, calculate_final_dmg

def calculate_total_def(def_char, def_pet):
    """
    คำนวณ Total DEF สำหรับ Biscuit (สูตรพิเศษ)
    Total_DEF = DEF_CHAR + DEF_PET + (675 * 10.5 / 100)
    Note: Formation bonus fixed at 10.5% (Frontline/Defense focus?)
    Note: No BUFF_ATK multiplier for DEF part as requested.
    """
    # 675 is base defense for support/defense potentially, user provided constant
    formation_bonus = Decimal("675") * Decimal("10.5") / Decimal("100")
    total_def = def_char + def_pet + formation_bonus
    return total_def

def calculate_biscuit_damage(
    total_atk: Decimal,
    skill_dmg_atk: Decimal, # SKILL_DMG (Attack part)
    skill_dmg_def: Decimal, # SKILL_DMG from Def (e.g. 135%)
    crit_dmg: Decimal,
    weak_dmg: Decimal,
    dmg_amp_buff: Decimal,
    dmg_amp_debuff: Decimal,
    dmg_reduction: Decimal,
    eff_def: Decimal,
    skill_hits: int,
    def_char: Decimal,
    def_pet: Decimal,
    final_dmg_hp: Decimal
) -> dict:
    """
    คำนวณดาเมจของ Biscuit (Dual Scaling: ATK + DEF)
    """
    # Calculate Total DEF
    # Formula: DEF_CHAR + DEF_PET + (Base_DEF_Support * Formation_DEF% / 100)
    # Base_DEF_Support (Legend) = 675
    # Formation_DEF = 10.5 (Fixed per user request)
    base_def_bonus = Decimal("675") * Decimal("10.5") / Decimal("100")
    total_def = def_char + def_pet + base_def_bonus
    
    # 2. RAW DMG 1 (ATK Based)
    # 2.1 Crit
    raw_dmg_1_crit = calculate_raw_dmg(
        total_atk, skill_dmg_atk, crit_dmg, Decimal("0"), 
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, final_dmg_hp
    )
    # 2.2 Normal (No Crit)
    raw_dmg_1_normal = calculate_raw_dmg(
        total_atk, skill_dmg_atk, Decimal("100"), Decimal("0"), 
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, final_dmg_hp
    )
    
    # 3. RAW DMG 2 (DEF Based)
    # 3.1 Crit
    raw_dmg_2_crit = calculate_raw_dmg(
        total_def, skill_dmg_def, crit_dmg, Decimal("0"),
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, Decimal("0")
    )
    # 3.2 Normal (No Crit)
    raw_dmg_2_normal = calculate_raw_dmg(
        total_def, skill_dmg_def, Decimal("100"), Decimal("0"),
        dmg_amp_buff, dmg_amp_debuff, dmg_reduction, Decimal("0")
    )
    
    # Calculate Final Damage per hit
    # Crit
    final_dmg_1_crit = calculate_final_dmg(raw_dmg_1_crit, eff_def)
    final_dmg_2_crit = calculate_final_dmg(raw_dmg_2_crit, eff_def)
    total_per_hit_crit = final_dmg_1_crit + final_dmg_2_crit
    
    # Normal
    final_dmg_1_normal = calculate_final_dmg(raw_dmg_1_normal, eff_def)
    final_dmg_2_normal = calculate_final_dmg(raw_dmg_2_normal, eff_def)
    total_per_hit_normal = final_dmg_1_normal + final_dmg_2_normal
    
    # Total Skill Damage
    total_skill_dmg_crit = total_per_hit_crit * Decimal(skill_hits)
    total_skill_dmg_normal = total_per_hit_normal * Decimal(skill_hits)

    return {
        "total_def": total_def,
        "raw_atk_crit": raw_dmg_1_crit,
        "raw_atk_normal": raw_dmg_1_normal,
        "raw_def_crit": raw_dmg_2_crit,
        "raw_def_normal": raw_dmg_2_normal,
        
        "final_atk_crit": final_dmg_1_crit,
        "final_atk_normal": final_dmg_1_normal,
        "final_def_crit": final_dmg_2_crit,
        "final_def_normal": final_dmg_2_normal,
        
        "total_per_hit_crit": total_per_hit_crit,
        "total_per_hit_normal": total_per_hit_normal,
        
        "total_skill_dmg_crit": total_skill_dmg_crit,
        "total_skill_dmg_normal": total_skill_dmg_normal,
        "skill_hits": skill_hits
    }

def print_biscuit_results(result):
    print("\n" + "="*50)
    print(f"Biscuit Calculation Results")
    print("="*50)
    
    print(f"Total DEF (Classic): {result['total_def']:,.0f}")
    print("-" * 40)
    print(f"{'Type':<10} | {'ATK Part':<12} | {'DEF Part':<12} | {'Total':<12}")
    print("-" * 40)
    
    print(f"{'Normal':<10} | {result['final_atk_normal']:<12,.0f} | {result['final_def_normal']:<12,.0f} | {result['total_per_hit_normal']:<12,.0f}")
    print(f"{'CRIT':<10} | {result['final_atk_crit']:<12,.0f} | {result['final_def_crit']:<12,.0f} | {result['total_per_hit_crit']:<12,.0f}")
    
    print("-" * 40)
    print(f"Total Skill Damage (Normal) {result['skill_hits']} hits: {result['total_skill_dmg_normal']:,.0f}")
    print(f"Total Skill Damage (CRIT)   {result['skill_hits']} hits: {result['total_skill_dmg_crit']:,.0f}")
    print("="*50)

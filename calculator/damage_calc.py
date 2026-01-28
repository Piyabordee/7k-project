"""
7k Rebirth Damage Calculator - Core Calculation Functions
สูตรการคำนวณดาเมจตาม AGENTS.md (แก้ไขแล้ว)
"""

from decimal import Decimal, ROUND_DOWN
from constants import DEF_MODIFIER, ATK_BASE

# Type alias for values that can be converted to Decimal
NumericType = int | float | str | Decimal


def to_decimal(value: NumericType) -> Decimal:
    """แปลงค่าเป็น Decimal"""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def calculate_total_atk(
    atk_char: Decimal,
    atk_pet: Decimal,
    atk_base: Decimal,
    formation: Decimal,
    potential_pet: Decimal,
    buff_atk: Decimal,
    buff_atk_pet: Decimal
) -> Decimal:
    """
    คำนวณ Total ATK (ผลรวมพลังโจมตี)
    
    สูตร: (ATK_CHAR + ATK_PET + (ATK_BASE * (Formation + Potential_PET) / 100)) 
          * (1 + ((BUFF_ATK + BUFF_ATK_PET) / 100))
    """
    formation_bonus = atk_base * (formation + potential_pet) / Decimal("100")
    base_atk = atk_char + atk_pet + formation_bonus
    buff_mult = Decimal("1") + (buff_atk + buff_atk_pet) / Decimal("100")
    return base_atk * buff_mult


def calculate_dmg_hp(
    hp_target: Decimal,
    bonus_dmg_hp_target: Decimal
) -> Decimal:
    """
    คำนวณ DMG_HP (ดาเมจจาก HP)
    
    สูตร: HP_Target * Bonus_DMG_HP_Target / 100
    """
    return hp_target * bonus_dmg_hp_target / Decimal("100")


def calculate_cap_atk(
    total_atk: Decimal,
    cap_atk_percent: Decimal
) -> Decimal:
    """
    คำนวณ Cap_ATK (แคปดาเมจ HP)
    
    สูตร: Total_ATK * Cap_ATK% / 100
    """
    return total_atk * cap_atk_percent / Decimal("100")


def calculate_final_dmg_hp(
    dmg_hp: Decimal,
    cap_atk: Decimal
) -> Decimal:
    """
    คำนวณ Final_DMG_HP (ดาเมจ HP สุดท้าย)
    
    สูตร: ROUNDDOWN(IF(DMG_HP > Cap_ATK, Cap_ATK, DMG_HP))
    """
    if dmg_hp > cap_atk and cap_atk > Decimal("0"):
        result = cap_atk
    else:
        result = dmg_hp
    return result.quantize(Decimal("1"), rounding=ROUND_DOWN)


def calculate_raw_dmg(
    total_atk: Decimal,
    skill_dmg: Decimal,
    crit_dmg: Decimal,
    weak_dmg: Decimal,
    dmg_amp_buff: Decimal,
    dmg_amp_debuff: Decimal,
    dmg_reduction: Decimal,
    final_dmg_hp: Decimal = Decimal("0")
) -> Decimal:
    """
    คำนวณ RAW Damage (ดาเมจดิบ)
    
    สูตร: 
    (Total_ATK * (SKILL_DMG/100) * (CRIT_DMG/100) 
     * (1 + WEAK_DMG/100) * (1 + DMG_AMP_BUFF/100) 
     * (1 + (DMG_AMP_DEBUFF - DMG_Reduction)/100))
    + (Final_DMG_HP * (CRIT_DMG/100) 
     * (1 + WEAK_DMG/100) * (1 + DMG_AMP_BUFF/100) 
     * (1 + (DMG_AMP_DEBUFF - DMG_Reduction)/100))
    """
    # ตัวคูณร่วม
    skill_mult = skill_dmg / Decimal("100")
    crit_mult = crit_dmg / Decimal("100")
    weak_mult = Decimal("1") + weak_dmg / Decimal("100")
    amp_buff_mult = Decimal("1") + dmg_amp_buff / Decimal("100")
    amp_debuff_reduction_mult = Decimal("1") + (dmg_amp_debuff - dmg_reduction) / Decimal("100")
    
    # ส่วนแรก: ดาเมจจาก ATK
    atk_dmg = total_atk * skill_mult * crit_mult * weak_mult * amp_buff_mult * amp_debuff_reduction_mult
    
    # ส่วนสอง: ดาเมจจาก HP-based
    hp_dmg = final_dmg_hp * crit_mult * weak_mult * amp_buff_mult * amp_debuff_reduction_mult
    
    return atk_dmg + hp_dmg


def calculate_effective_def(
    def_target: Decimal,
    def_buff: Decimal,
    def_reduce: Decimal,
    ignore_def: Decimal
) -> Decimal:
    """
    คำนวณ Effective DEF (ตัวหารจาก DEF)
    
    สูตร: 1 + (DEF_Modifier * DEF_Target * ((1 + DEF_BUFF/100 - DEF_REDUCE/100) * (1 - Ignore_DEF/100)))
    """
    def_mult = Decimal("1") + def_buff / Decimal("100") - def_reduce / Decimal("100")
    ignore_mult = Decimal("1") - ignore_def / Decimal("100")
    effective = Decimal("1") + (DEF_MODIFIER * def_target * def_mult * ignore_mult)
    return effective


def calculate_final_dmg(
    raw_dmg: Decimal,
    effective_def: Decimal
) -> int:
    """
    คำนวณ Final Damage (ดาเมจสุดท้าย)
    
    สูตร: ROUNDDOWN(RAW_DMG / Effective_DEF)
    """
    final = raw_dmg / effective_def
    return int(final.quantize(Decimal("1"), rounding=ROUND_DOWN))

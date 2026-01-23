"""
Freyja Special Logic - HP Alteration Calculator
HP Alteration = ปรับ HP เป้าหมายเหลือ X% (ไม่ใช่เพิ่มดาเมจ)
"""

from __future__ import annotations

from decimal import Decimal, ROUND_DOWN
from typing import Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from damage_calc import calculate_total_atk, calculate_raw_dmg, calculate_effective_def


def calculate_hp_alteration_damage(hp_target: Decimal, hp_alteration_percent: Decimal) -> int:
    """
    คำนวณดาเมจจาก HP Alteration
    HP Alteration = ปรับ HP มอนเตอร์เหลือ X%
    ดาเมจ = HP_Target × (100% - HP_Alteration%)
    
    ตัวอย่าง: HP_Target = 100,000, HP_Alteration = 39%
    ดาเมจ = 100,000 × (100 - 39)/100 = 100,000 × 0.61 = 61,000
    """
    damage_percent = (Decimal("100") - hp_alteration_percent) / Decimal("100")
    damage = hp_target * damage_percent
    return int(damage.quantize(Decimal("1"), rounding=ROUND_DOWN))


def calculate_freyja_damage(
    total_atk: Decimal,
    skill_dmg: Decimal,
    crit_dmg: Decimal,
    weak_dmg: Decimal,
    dmg_amp_buff: Decimal,
    dmg_amp_debuff: Decimal,
    dmg_reduction: Decimal,
    eff_def: Decimal,
    skill_hits: int,
    hp_target: Decimal,
    hp_alteration: Decimal
) -> dict[str, Any]:
    """
    คำนวณดาเมจ Freyja ทั้ง 4 กรณี:
    1. ดาเมจคริปกติ (ไม่มี HP Alteration)
    2. ดาเมจคริ + HP Alteration
    3. ดาเมจติดจุดอ่อน (ไม่มี HP Alteration)
    4. ดาเมจติดจุดอ่อน + HP Alteration
    """
    
    # Base weakness (30%) + WEAK_DMG from config/character
    base_weakness = Decimal("30")
    total_weakness = base_weakness + weak_dmg
    
    # === กรณี 1: ดาเมจคริปกติ (ไม่มี HP Alteration) ===
    raw_crit = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=Decimal("0"),
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=Decimal("0")
    )
    final_crit = int((raw_crit / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === กรณี 2: HP Alteration damage ===
    hp_alter_damage = calculate_hp_alteration_damage(hp_target, hp_alteration)
    
    # === กรณี 3: ดาเมจติดจุดอ่อน (ไม่มี HP Alteration) ===
    raw_weak = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=total_weakness,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=Decimal("0")
    )
    final_weak = int((raw_weak / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    return {
        "crit_damage": final_crit,
        "crit_per_hit": final_crit // skill_hits if skill_hits > 0 else final_crit,
        "hp_alteration_damage": hp_alter_damage,
        "weakness_damage": final_weak,
        "weakness_per_hit": final_weak // skill_hits if skill_hits > 0 else final_weak,
        "hp_alteration_percent": hp_alteration,
        "total_weakness_percent": total_weakness,
        "skill_hits": skill_hits
    }


def print_freyja_results(results: dict[str, Any], hp_target: Decimal) -> None:
    """แสดงผลลัพธ์ Freyja แบบเต็ม"""
    hits = results["skill_hits"]
    hp_alt = results["hp_alteration_percent"]
    
    print("\n" + "=" * 50)
    print("  🌟 Freyja - HP Alteration Calculator 🌟")
    print("=" * 50)
    
    print(f"\n  📊 HP Target: {hp_target:,.0f}")
    print(f"  ⚡ HP Alteration: {hp_alt}% (มอนเหลือ {hp_alt}%)")
    
    print("\n" + "-" * 50)
    print("  ดาเมจปกติ (สกิล)")
    print("-" * 50)
    print(f"  ดาเมจคริ:        {results['crit_damage']:,}")
    if hits > 1:
        print(f"                   ({hits} hits x {results['crit_per_hit']:,}/hit)")
    
    print(f"  ดาเมจติดจุดอ่อน: {results['weakness_damage']:,} (+{results['total_weakness_percent']:.0f}%)")
    if hits > 1:
        print(f"                   ({hits} hits x {results['weakness_per_hit']:,}/hit)")
    
    print("\n" + "-" * 50)
    print("  ดาเมจ HP Alteration (ถ้ามี 4 Divinity stacks)")
    print("-" * 50)
    print(f"  HP Alteration:   {results['hp_alteration_damage']:,}")
    print(f"                   (มอนเหลือ {hp_alt}% จาก {hp_target:,.0f} HP)")
    
    print("\n" + "-" * 50)
    print("  ดาเมจรวม (สกิล + HP Alteration)")
    print("-" * 50)
    total_crit = results['crit_damage'] + results['hp_alteration_damage']
    total_weak = results['weakness_damage'] + results['hp_alteration_damage']
    print(f"  คริ + HP Alt:        {total_crit:,}")
    print(f"  จุดอ่อน + HP Alt:    {total_weak:,}")
    
    print("\n" + "=" * 50)

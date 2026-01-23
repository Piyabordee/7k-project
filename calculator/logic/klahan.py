"""
Klahan Special Logic - HP Condition Bonus Calculator
- Skill 1 (Gale Blast): +135% bonus เมื่อ HP >= 50%
- Skill 2 (Flying Tiger): +115% bonus เมื่อ HP <= 50%
"""

from __future__ import annotations

from decimal import Decimal, ROUND_DOWN
from typing import Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from damage_calc import calculate_raw_dmg


def calculate_klahan_damage(
    total_atk: Decimal,
    skill_dmg: Decimal,
    hp_above_50_bonus: Decimal,
    hp_below_50_bonus: Decimal,
    crit_dmg: Decimal,
    weak_dmg: Decimal,
    dmg_amp_buff: Decimal,
    dmg_amp_debuff: Decimal,
    dmg_reduction: Decimal,
    eff_def: Decimal,
    skill_hits: int,
    skill_name: str
) -> dict[str, Any]:
    """
    คำนวณดาเมจ Klahan ทั้ง 4 กรณี:
    1. ดาเมจคริ (ไม่มี HP bonus)
    2. ดาเมจคริ + HP bonus
    3. ดาเมจติดจุดอ่อน (ไม่มี HP bonus)
    4. ดาเมจติดจุดอ่อน + HP bonus
    """
    
    # Base weakness (30%) + WEAK_DMG from config/character
    base_weakness = Decimal("30")
    total_weakness = base_weakness + weak_dmg
    
    # Determine HP bonus based on skill type
    hp_bonus = Decimal("0")
    hp_condition = ""
    if hp_above_50_bonus > 0:
        hp_bonus = hp_above_50_bonus
        hp_condition = "HP >= 50%"
    elif hp_below_50_bonus > 0:
        hp_bonus = hp_below_50_bonus
        hp_condition = "HP <= 50%"
    
    # === กรณี 1: ดาเมจคริ (ไม่มี HP bonus) ===
    raw_crit_no_bonus = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=Decimal("0"),
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=Decimal("0")
    )
    final_crit_no_bonus = int((raw_crit_no_bonus / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === กรณี 2: ดาเมจคริ + HP bonus ===
    skill_dmg_with_bonus = skill_dmg + hp_bonus
    raw_crit_with_bonus = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg_with_bonus,
        crit_dmg=crit_dmg,
        weak_dmg=Decimal("0"),
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=Decimal("0")
    )
    final_crit_with_bonus = int((raw_crit_with_bonus / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === กรณี 3: ดาเมจติดจุดอ่อน (ไม่มี HP bonus) ===
    raw_weak_no_bonus = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=total_weakness,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=Decimal("0")
    )
    final_weak_no_bonus = int((raw_weak_no_bonus / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === กรณี 4: ดาเมจติดจุดอ่อน + HP bonus ===
    raw_weak_with_bonus = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg_with_bonus,
        crit_dmg=crit_dmg,
        weak_dmg=total_weakness,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=Decimal("0")
    )
    final_weak_with_bonus = int((raw_weak_with_bonus / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    return {
        "crit_no_bonus": {
            "raw": raw_crit_no_bonus,
            "final": final_crit_no_bonus * skill_hits,
            "per_hit": final_crit_no_bonus
        },
        "crit_with_bonus": {
            "raw": raw_crit_with_bonus,
            "final": final_crit_with_bonus * skill_hits,
            "per_hit": final_crit_with_bonus
        },
        "weak_no_bonus": {
            "raw": raw_weak_no_bonus,
            "final": final_weak_no_bonus * skill_hits,
            "per_hit": final_weak_no_bonus
        },
        "weak_with_bonus": {
            "raw": raw_weak_with_bonus,
            "final": final_weak_with_bonus * skill_hits,
            "per_hit": final_weak_with_bonus
        },
        "skill_hits": skill_hits,
        "skill_name": skill_name,
        "skill_dmg": skill_dmg,
        "hp_bonus": hp_bonus,
        "hp_condition": hp_condition,
        "total_skill_dmg": skill_dmg_with_bonus,
        "total_weakness": total_weakness
    }


def print_klahan_results(results: dict[str, Any]) -> None:
    """แสดงผลลัพธ์ Klahan แบบเต็ม"""
    hits = results["skill_hits"]
    skill_name = results["skill_name"]
    skill_dmg = results["skill_dmg"]
    hp_bonus = results["hp_bonus"]
    hp_cond = results["hp_condition"]
    total_dmg = results["total_skill_dmg"]
    
    print("\n" + "=" * 60)
    print(f"  🐯 Klahan - {skill_name} Calculator 🐯")
    print("=" * 60)
    
    print(f"\n  📊 Base SKILL_DMG: {skill_dmg}%")
    print(f"  ⚡ HP Bonus: +{hp_bonus}% (เมื่อ {hp_cond})")
    print(f"  🔥 Total SKILL_DMG: {total_dmg}%")
    
    # กรณี 1: คริ ไม่มี bonus
    print("\n" + "-" * 60)
    print(f"  [1] ดาเมจคริ (HP ไม่ตรงเงื่อนไข)")
    print("-" * 60)
    r = results["crit_no_bonus"]
    print(f"  Final: {r['final']:,} (SKILL_DMG: {skill_dmg}%)")
    if hits > 1:
        print(f"         ({hits} hits x {r['per_hit']:,}/hit)")
    
    # กรณี 2: คริ + HP bonus
    print("\n" + "-" * 60)
    print(f"  [2] ดาเมจคริ ({hp_cond}) 🔥")
    print("-" * 60)
    r = results["crit_with_bonus"]
    print(f"  Final: {r['final']:,} (SKILL_DMG: {total_dmg}%)")
    if hits > 1:
        print(f"         ({hits} hits x {r['per_hit']:,}/hit)")
    
    # กรณี 3: จุดอ่อน ไม่มี bonus
    print("\n" + "-" * 60)
    print(f"  [3] ดาเมจติดจุดอ่อน (HP ไม่ตรงเงื่อนไข)")
    print("-" * 60)
    r = results["weak_no_bonus"]
    print(f"  Final: {r['final']:,} (SKILL_DMG: {skill_dmg}%)")
    if hits > 1:
        print(f"         ({hits} hits x {r['per_hit']:,}/hit)")
    
    # กรณี 4: จุดอ่อน + HP bonus (MAX DAMAGE)
    print("\n" + "-" * 60)
    print(f"  [4] ดาเมจติดจุดอ่อน ({hp_cond}) 🔥 MAX")
    print("-" * 60)
    r = results["weak_with_bonus"]
    print(f"  Final: {r['final']:,} (SKILL_DMG: {total_dmg}%)")
    if hits > 1:
        print(f"         ({hits} hits x {r['per_hit']:,}/hit)")
    
    print("\n" + "=" * 60)
    print(f"  💀 ดาเมจสูงสุด: {results['weak_with_bonus']['final']:,}")
    print("=" * 60)

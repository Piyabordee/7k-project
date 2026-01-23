"""
Ryan Special Logic - Lost HP Bonus & Weakness Extra Damage Calculator
- Lost HP Bonus: ดาเมจเพิ่มได้ถึง X% ตาม HP ที่เสียไปของเป้าหมาย
- WEAK_SKILL_DMG: ดาเมจเสริมเมื่อติดจุดอ่อน
"""

from __future__ import annotations

from decimal import Decimal, ROUND_DOWN
from typing import Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from damage_calc import calculate_total_atk, calculate_raw_dmg, calculate_effective_def


def calculate_lost_hp_multiplier(target_hp_percent: Decimal, max_bonus: Decimal) -> Decimal:
    """
    คำนวณ Lost HP Bonus multiplier
    
    สูตร: ดาเมจเพิ่มตามสัดส่วน HP ที่เสียไป
    - HP เต็ม (100%) = ไม่มี bonus (1.00x)
    - HP เหลือ 0% = bonus เต็ม (1.00 + max_bonus/100)
    
    ตัวอย่าง: max_bonus = 50%, HP เหลือ 30%
    lost_hp = 70%
    bonus = 50% × 0.70 = 35%
    multiplier = 1.35
    """
    # HP ที่เสียไป (0-100%)
    lost_hp_percent = Decimal("100") - target_hp_percent
    if lost_hp_percent < 0:
        lost_hp_percent = Decimal("0")
    if lost_hp_percent > 100:
        lost_hp_percent = Decimal("100")
    
    # Bonus ตามสัดส่วน
    bonus_percent = max_bonus * lost_hp_percent / Decimal("100")
    
    return Decimal("1") + bonus_percent / Decimal("100")


def calculate_ryan_damage(
    total_atk: Decimal,
    skill_dmg: Decimal,
    weak_skill_dmg: Decimal,
    crit_dmg: Decimal,
    weak_dmg: Decimal,
    dmg_amp_buff: Decimal,
    dmg_amp_debuff: Decimal,
    dmg_reduction: Decimal,
    eff_def: Decimal,
    skill_hits: int,
    lost_hp_bonus: Decimal,
    target_hp_percent: Decimal
) -> dict[str, Any]:
    """
    คำนวณดาเมจ Ryan ทั้ง 4 กรณี:
    1. ดาเมจคริ (HP เต็ม)
    2. ดาเมจคริ (HP ต่ำ - Lost HP Bonus เต็ม)
    3. ดาเมจติดจุดอ่อน (HP เต็ม) - ใช้ WEAK_SKILL_DMG
    4. ดาเมจติดจุดอ่อน (HP ต่ำ) - ใช้ WEAK_SKILL_DMG + Lost HP Bonus
    """
    
    # Base weakness (30%) + WEAK_DMG from config/character
    base_weakness = Decimal("30")
    total_weakness = base_weakness + weak_dmg
    
    # Lost HP multiplier (สูงสุดเมื่อ HP เหลือ 0%)
    lost_hp_mult_min = Decimal("1")  # HP เต็ม
    lost_hp_mult_max = calculate_lost_hp_multiplier(target_hp_percent, lost_hp_bonus)
    
    # === กรณี 1: ดาเมจคริ (HP เต็ม) ===
    raw_crit_full = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=Decimal("0"),
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=Decimal("0")
    )
    final_crit_full = int((raw_crit_full / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === กรณี 2: ดาเมจคริ (HP ต่ำ - Lost HP Bonus) ===
    raw_crit_low = raw_crit_full * lost_hp_mult_max
    final_crit_low = int((raw_crit_low / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === กรณี 3: ดาเมจติดจุดอ่อน (HP เต็ม) ===
    # Ryan พิเศษ: ใช้ WEAK_SKILL_DMG แทน SKILL_DMG เมื่อติดจุดอ่อน
    total_skill_dmg_weak = skill_dmg + weak_skill_dmg  # รวมดาเมจ
    raw_weak_full = calculate_raw_dmg(
        total_atk=total_atk,
        skill_dmg=total_skill_dmg_weak,
        crit_dmg=crit_dmg,
        weak_dmg=total_weakness,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        final_dmg_hp=Decimal("0")
    )
    final_weak_full = int((raw_weak_full / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    # === กรณี 4: ดาเมจติดจุดอ่อน (HP ต่ำ - Lost HP Bonus) ===
    raw_weak_low = raw_weak_full * lost_hp_mult_max
    final_weak_low = int((raw_weak_low / eff_def).quantize(Decimal("1"), rounding=ROUND_DOWN))
    
    return {
        "crit_full_hp": {
            "raw": raw_crit_full,
            "final": final_crit_full * skill_hits,
            "per_hit": final_crit_full
        },
        "crit_low_hp": {
            "raw": raw_crit_low,
            "final": final_crit_low * skill_hits,
            "per_hit": final_crit_low,
            "multiplier": lost_hp_mult_max
        },
        "weak_full_hp": {
            "raw": raw_weak_full,
            "final": final_weak_full * skill_hits,
            "per_hit": final_weak_full
        },
        "weak_low_hp": {
            "raw": raw_weak_low,
            "final": final_weak_low * skill_hits,
            "per_hit": final_weak_low,
            "multiplier": lost_hp_mult_max
        },
        "skill_hits": skill_hits,
        "lost_hp_bonus": lost_hp_bonus,
        "target_hp_percent": target_hp_percent,
        "weak_skill_dmg": weak_skill_dmg,
        "total_weakness": total_weakness
    }


def print_ryan_results(results: dict[str, Any]) -> None:
    """แสดงผลลัพธ์ Ryan แบบเต็ม"""
    hits = results["skill_hits"]
    lost_hp = results["lost_hp_bonus"]
    target_hp = results["target_hp_percent"]
    weak_extra = results["weak_skill_dmg"]
    
    print("\n" + "=" * 60)
    print("  ⚔️ Ryan - Gale Slash Calculator ⚔️")
    print("=" * 60)
    
    print(f"\n  📊 HP เป้าหมายเหลือ: {target_hp}%")
    print(f"  ⚡ Lost HP Bonus: สูงสุด +{lost_hp}%")
    print(f"  🔥 Weakness Extra Damage: +{weak_extra}%")
    
    # กรณี 1: คริ HP เต็ม
    print("\n" + "-" * 60)
    print("  [1] ดาเมจคริ (HP เต็ม 100%)")
    print("-" * 60)
    r = results["crit_full_hp"]
    print(f"  Final: {r['final']:,}")
    if hits > 1:
        print(f"         ({hits} hits x {r['per_hit']:,}/hit)")
    
    # กรณี 2: คริ HP ต่ำ
    print("\n" + "-" * 60)
    print(f"  [2] ดาเมจคริ (HP เหลือ {target_hp}%)")
    print("-" * 60)
    r = results["crit_low_hp"]
    bonus_pct = (r['multiplier'] - 1) * 100
    print(f"  Final: {r['final']:,} (+{bonus_pct:.1f}% Lost HP Bonus)")
    if hits > 1:
        print(f"         ({hits} hits x {r['per_hit']:,}/hit)")
    
    # กรณี 3: จุดอ่อน HP เต็ม
    print("\n" + "-" * 60)
    print(f"  [3] ดาเมจติดจุดอ่อน (HP เต็ม 100%)")
    print("-" * 60)
    r = results["weak_full_hp"]
    print(f"  Final: {r['final']:,} (+{weak_extra}% Weakness Extra)")
    if hits > 1:
        print(f"         ({hits} hits x {r['per_hit']:,}/hit)")
    
    # กรณี 4: จุดอ่อน HP ต่ำ (MAX DAMAGE)
    print("\n" + "-" * 60)
    print(f"  [4] ดาเมจติดจุดอ่อน (HP เหลือ {target_hp}%) 🔥 MAX")
    print("-" * 60)
    r = results["weak_low_hp"]
    bonus_pct = (r['multiplier'] - 1) * 100
    print(f"  Final: {r['final']:,}")
    print(f"         (+{weak_extra}% Weakness Extra, +{bonus_pct:.1f}% Lost HP)")
    if hits > 1:
        print(f"         ({hits} hits x {r['per_hit']:,}/hit)")
    
    print("\n" + "=" * 60)
    print(f"  💀 ดาเมจสูงสุด: {results['weak_low_hp']['final']:,}")
    print("=" * 60)

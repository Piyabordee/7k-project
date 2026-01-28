"""
Character Registry - Registry pattern for character-specific logic
แต่ละตัวละคร register logic ของตัวเองเพื่อลดการใช้ if/elif ใน main.py
"""

from decimal import Decimal
from typing import Any, Callable, Protocol


class CharacterHandler(Protocol):
    """Protocol สำหรับ character handler function"""

    def __call__(
        self,
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
        config: dict[str, Any],
        char_meta: dict[str, Any],
        skill_config: dict[str, Any],
        monster_preset: dict[str, Any] | None,
    ) -> bool:
        """
        Handler function สำหรับตัวละคร
        Returns True ถ้า handle แล้ว, False ถ้าไม่ใช่ตัวละครนี้
        """
        ...


# Registry เก็บ handler ของแต่ละตัวละคร
_CHARACTER_HANDLERS: dict[str, CharacterHandler] = {}


def register_character(name: str) -> Callable[[CharacterHandler], CharacterHandler]:
    """
    Decorator สำหรับ register character handler

    การใช้งาน:
    @register_character("freyja")
    def handle_freyja(...):
        ...
    """

    def decorator(handler: CharacterHandler) -> CharacterHandler:
        _CHARACTER_HANDLERS[name.lower()] = handler
        return handler

    return decorator


def get_character_handler(name: str) -> CharacterHandler | None:
    """ดึง handler ของตัวละครจาก registry"""
    return _CHARACTER_HANDLERS.get(name.lower())


def list_registered_characters() -> list[str]:
    """แสดงรายชื่อตัวละครทั้งหมดที่มี handler"""
    return list(_CHARACTER_HANDLERS.keys())


# ============================================
# Character Handlers
# ============================================

@register_character("freyja")
def handle_freyja(
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
    config: dict[str, Any],
    char_meta: dict[str, Any],
    skill_config: dict[str, Any],
    monster_preset: dict[str, Any] | None,
) -> bool:
    """Handler สำหรับ Freyja - ใช้ HP Alteration logic"""
    from decimal import Decimal as D
    from logic.freyja import calculate_freyja_damage, print_freyja_results

    hp_alteration = config.get("HP_Alteration", D("0"))
    is_both_skills = skill_config.get("_is_both_skills", False)

    if hp_alteration <= 0 or is_both_skills:
        return False

    result = calculate_freyja_damage(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=weak_dmg,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        eff_def=eff_def,
        skill_hits=skill_hits,
        hp_target=hp_target,
        hp_alteration=hp_alteration,
    )

    print_freyja_results(result, hp_target)
    return True


@register_character("ryan")
def handle_ryan(
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
    config: dict[str, Any],
    char_meta: dict[str, Any],
    skill_config: dict[str, Any],
    monster_preset: dict[str, Any] | None,
) -> bool:
    """Handler สำหรับ Ryan - ใช้ Lost HP Bonus logic"""
    from decimal import Decimal as D
    from logic.ryan import calculate_ryan_damage, print_ryan_results

    lost_hp_bonus = config.get("Lost_HP_Bonus", D("0"))
    weak_skill_dmg = config.get("WEAK_SKILL_DMG", D("0"))
    target_hp_percent = config.get("Target_HP_Percent", D("100"))
    is_both_skills = skill_config.get("_is_both_skills", False)

    if lost_hp_bonus <= 0 or is_both_skills:
        return False

    result = calculate_ryan_damage(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        weak_skill_dmg=weak_skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=weak_dmg,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        eff_def=eff_def,
        skill_hits=skill_hits,
        lost_hp_bonus=lost_hp_bonus,
        target_hp_percent=target_hp_percent,
    )

    print_ryan_results(result)
    return True


@register_character("klahan")
def handle_klahan(
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
    config: dict[str, Any],
    char_meta: dict[str, Any],
    skill_config: dict[str, Any],
    monster_preset: dict[str, Any] | None,
) -> bool:
    """Handler สำหรับ Klahan - ใช้ HP condition bonus logic"""
    from decimal import Decimal as D
    from logic.klahan import calculate_klahan_damage, print_klahan_results

    hp_above_50_bonus = config.get("HP_Above_50_Bonus", D("0"))
    hp_below_50_bonus = config.get("HP_Below_50_Bonus", D("0"))
    is_both_skills = skill_config.get("_is_both_skills", False)

    if (hp_above_50_bonus <= 0 and hp_below_50_bonus <= 0) or is_both_skills:
        return False

    # ดึงชื่อสกิล
    skill_name_display = skill_config.get("_name", "Skill")
    if "_name" not in skill_config:
        skills = char_meta.get("_skills", {})
        for key, val in skills.items():
            if val.get("HP_Above_50_Bonus") == float(hp_above_50_bonus) or val.get(
                "HP_Below_50_Bonus"
            ) == float(hp_below_50_bonus):
                skill_name_display = val.get("_name", key)
                break

    result = calculate_klahan_damage(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        hp_above_50_bonus=hp_above_50_bonus,
        hp_below_50_bonus=hp_below_50_bonus,
        crit_dmg=crit_dmg,
        weak_dmg=weak_dmg,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        eff_def=eff_def,
        skill_hits=skill_hits,
        skill_name=skill_name_display,
    )

    print_klahan_results(result)
    return True


@register_character("sun_wukong")
def handle_sun_wukong(
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
    config: dict[str, Any],
    char_meta: dict[str, Any],
    skill_config: dict[str, Any],
    monster_preset: dict[str, Any] | None,
) -> bool:
    """Handler สำหรับ Sun Wukong - ใช้ Castle Mode logic"""
    from decimal import Decimal as D
    from logic.sun_wukong import calculate_sun_wukong_castle_mode, print_castle_mode_results

    is_both_skills = skill_config.get("_is_both_skills", False)

    if not monster_preset or is_both_skills:
        return False

    # ดึงชื่อสกิล
    skill_name_display = skill_config.get("_name", "Skill")
    if "_name" not in skill_config:
        skills = char_meta.get("_skills", {})
        for key, val in skills.items():
            if val.get("SKILL_DMG") == float(skill_dmg):
                skill_name_display = val.get("_name", key)
                break

    result = calculate_sun_wukong_castle_mode(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=weak_dmg,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        eff_def=eff_def,
        skill_hits=skill_hits,
        hp_target=hp_target,
        skill_name=skill_name_display,
        final_dmg_hp=config.get("Final_DMG_HP", D("0")),
    )

    print_castle_mode_results(result)
    return True


@register_character("espada")
def handle_espada(
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
    config: dict[str, Any],
    char_meta: dict[str, Any],
    skill_config: dict[str, Any],
    monster_preset: dict[str, Any] | None,
) -> bool:
    """Handler สำหรับ Espada - ใช้ Bonus DMG HP Target logic"""
    from decimal import Decimal as D
    from logic.espada import calculate_espada_damage
    from display import print_espada_results

    bonus_dmg_hp_target = config.get("Bonus_DMG_HP_Target", D("0"))
    cap_atk_percent = config.get("Cap_ATK_Percent", D("0"))
    is_both_skills = skill_config.get("_is_both_skills", False)

    if bonus_dmg_hp_target <= 0 or is_both_skills:
        return False

    result = calculate_espada_damage(
        total_atk=total_atk,
        skill_dmg=skill_dmg,
        crit_dmg=crit_dmg,
        weak_dmg=weak_dmg,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        effective_def=eff_def,
        hp_target=hp_target,
        bonus_dmg_hp_target=bonus_dmg_hp_target,
        cap_atk_percent=cap_atk_percent,
    )

    print_espada_results(result, weak_dmg, config.get("Final_DMG_HP", D("0")))
    return True


@register_character("biscuit")
def handle_biscuit(
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
    config: dict[str, Any],
    char_meta: dict[str, Any],
    skill_config: dict[str, Any],
    monster_preset: dict[str, Any] | None,
) -> bool:
    """Handler สำหรับ Biscuit - ใช้ Dual Scaling ATK + DEF logic"""
    from decimal import Decimal as D
    from logic.biscuit import calculate_biscuit_damage, print_biscuit_results

    # อ่านค่า DEF_CHAR, DEF_PET จาก config
    print("\n--- Biscuit Special Stats Input ---")
    try:
        default_def_char = config.get("DEF_CHAR", "0")
        in_def_char = input(f"Enter DEF_CHAR (Default {default_def_char}): ").strip()
        def_char = D(in_def_char) if in_def_char else D(str(default_def_char))

        default_def_pet = config.get("DEF_PET", "0")
        in_def_pet = input(f"Enter DEF_PET (Default {default_def_pet}): ").strip()
        def_pet = D(in_def_pet) if in_def_pet else D(str(default_def_pet))
    except ValueError as e:
        print(f"Input Error: {e}. Using config values.")
        from config_loader import get_decimal

        def_char = get_decimal(config, "DEF_CHAR", "0")
        def_pet = get_decimal(config, "DEF_PET", "0")

    skill_dmg_from_def = config.get("SKILL_DMG_DEF", D("0"))

    result = calculate_biscuit_damage(
        total_atk=total_atk,
        skill_dmg_atk=skill_dmg,
        skill_dmg_def=skill_dmg_from_def,
        crit_dmg=crit_dmg,
        weak_dmg=weak_dmg,
        dmg_amp_buff=dmg_amp_buff,
        dmg_amp_debuff=dmg_amp_debuff,
        dmg_reduction=dmg_reduction,
        eff_def=eff_def,
        skill_hits=skill_hits,
        def_char=def_char,
        def_pet=def_pet,
        final_dmg_hp=config.get("Final_DMG_HP", D("0")),
    )

    print_biscuit_results(result)

    # Castle Mode Check
    if monster_preset and monster_preset.get("HP_Target"):
        hp_target_calc = D(monster_preset["HP_Target"])
        dmg_normal = result["total_skill_dmg_normal"]
        dmg_crit = result["total_skill_dmg_crit"]

        from display import print_kill_status_block

        print_kill_status_block(hp_target_calc, dmg_crit, "คริ", dmg_normal, "ธรรมดา")

    return True

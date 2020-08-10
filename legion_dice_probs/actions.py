from typing import Optional

from legion_dice_probs.events import convert_symbols as conv_syms
from legion_dice_probs.events import convert_surge_with_tokens as conv_srge_wtok
from legion_dice_probs.events import count_symbols as count_syms
from legion_dice_probs.events import roll as rll
from legion_dice_probs.events import aim_reroll as aim_rerll
from legion_dice_probs.events.tools import conversion_policy as conv_pol
from legion_dice_probs.events.tools import roll_policy as rll_pol
from legion_dice_probs.stochastic_states import symbol as sym

convert_all_surges_to_hit = conv_syms.ConvertSymbols(
    conversion_policy=conv_pol.get_conversion_policy_attack(
        convertible_symbols=(sym.Surge,),
        conversion_target=sym.Hit(),
    )
)

convert_all_surges_to_crit = conv_syms.ConvertSymbols(
    conversion_policy=conv_pol.get_conversion_policy_attack(
        convertible_symbols=(sym.Surge,),
        conversion_target=sym.Crit(),
    )
)

convert_all_surges_to_block = conv_syms.ConvertSymbols(
    conversion_policy=conv_pol.get_conversion_policy_defence(
        convertible_symbols=(sym.Surge,),
        conversion_target=sym.Block(),
    )
)


def get_use_surge_tokens_attack(k: Optional[int] = None):
    return conv_srge_wtok.ConvertSurgeWithTokens(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Surge,),
            conversion_target=sym.Hit(),
        ),
        conversion_limit=k,  # Specified by actual number of available tokens in stochastic object/state.
    )


use_surge_tokens_attack_1 = get_use_surge_tokens_attack(1)
use_surge_tokens_attack = get_use_surge_tokens_attack()


def get_use_surge_tokens_defence(k: Optional[int] = None):
    return conv_srge_wtok.ConvertSurgeWithTokens(
        conversion_policy=conv_pol.get_conversion_policy_defence(
            convertible_symbols=(sym.Surge,),
            conversion_target=sym.Block(),
        ),
        conversion_limit=k,  # Specified by actual number of available tokens in stochastic object/state.
    )


use_surge_tokens_defence_1 = get_use_surge_tokens_defence(1)
use_surge_tokens_defence = get_use_surge_tokens_defence()


def get_critical(k: int):
    return conv_syms.ConvertSymbols(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Surge,),
            conversion_target=sym.Crit(),
        ),
        conversion_limit=k,
    )


critical_1 = get_critical(1)
critical_2 = get_critical(2)
critical_3 = get_critical(3)


def get_ram(k: int):
    return conv_syms.ConvertSymbols(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Blank, sym.Surge, sym.Hit,),
            conversion_target=sym.Crit(),
        ),
        conversion_limit=k,
    )


ram_1 = get_ram(1)
ram_2 = get_ram(2)


def get_impact(k: int):
    return conv_syms.ConvertSymbols(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Hit,),
            conversion_target=sym.Crit(),
        ),
        conversion_limit=k,
    )


impact_1 = get_impact(1)
impact_2 = get_impact(2)
impact_3 = get_impact(3)
impact_4 = get_impact(4)


def block_hits(k: Optional[int]):
    return conv_syms.ConvertSymbols(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Hit,),
            conversion_target=sym.Blank(),
        ),
        conversion_limit=k,
    )


dodge_token = block_hits(1)
cover_1 = block_hits(1)
cover_2 = block_hits(2)
armour_1 = block_hits(1)
armour_2 = block_hits(2)
armour = block_hits(None)


def get_pierce(k: int):
    return conv_syms.ConvertSymbols(
        conversion_policy=conv_pol.get_conversion_policy_defence(
            convertible_symbols=(sym.Block,),
            conversion_target=sym.Blank(),
        ),
        conversion_limit=k,
    )


pierce_1 = get_pierce(1)
pierce_2 = get_pierce(2)
pierce_3 = get_pierce(3)


def get_attack_reroll(k: int):
    return rll.Roll(
        roll_policy=rll_pol.get_roll_policy_attack(
            rollable_symbols=(sym.Blank, sym.Surge,),
        ),
        roll_limit=k,
    )


def get_attack_reroll_aim_token(k: int):
    return aim_rerll.AimReroll(
        roll_policy=rll_pol.get_roll_policy_attack(
            rollable_symbols=(sym.Blank, sym.Surge,),
        ),
        roll_limit=k,
    )


# aim = get_attack_reroll(2)
aim = get_attack_reroll_aim_token(2)
aim_precise_1 = get_attack_reroll(3)
aim_precise_2 = get_attack_reroll(4)
aim_precise_3 = get_attack_reroll(5)


def get_defence_reroll(k: int):
    return rll.Roll(
        roll_policy=rll_pol.get_roll_policy_defence(
            rollable_symbols=(sym.Blank, sym.Surge,),
        ),
        roll_limit=k,
    )


uncanny_luck_3 = get_attack_reroll(3)

remove_unconverted_surge_results_attack = conv_syms.ConvertSymbols(
    conversion_policy=conv_pol.get_conversion_policy_attack(
        convertible_symbols=(sym.Surge,),
        conversion_target=sym.Blank(),
    )
)

remove_unconverted_surge_results_defence = conv_syms.ConvertSymbols(
    conversion_policy=conv_pol.get_conversion_policy_defence(
        convertible_symbols=(sym.Surge,),
        conversion_target=sym.Blank(),
    )
)

count_symbols = count_syms.CountSymbols()

convert_all_crits_to_hits_for_calculation = conv_syms.ConvertSymbols(
    conversion_policy=conv_pol.get_conversion_policy_attack(
        convertible_symbols=(sym.Crit,),
        conversion_target=sym.Hit(),
    )
)


# remove_tokens_for_cal

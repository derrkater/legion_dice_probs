from typing import Optional

from legion_dice_probs.events import convert_symbols as conv_syms
from legion_dice_probs.events import count_symbols as count_syms
from legion_dice_probs.events import roll as rll
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

surge_token_attack = conv_syms.ConvertSymbols(
    conversion_policy=conv_pol.get_conversion_policy_attack(
        convertible_symbols=(sym.Surge,),
        conversion_target=sym.Hit(),
    ),
    conversion_limit=1,
)

surge_token_defence = conv_syms.ConvertSymbols(
    conversion_policy=conv_pol.get_conversion_policy_defence(
        convertible_symbols=(sym.Surge,),
        conversion_target=sym.Block(),
    ),
    conversion_limit=1,
)


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


def get_attack_reroll(k: int):
    return rll.Roll(
        roll_policy=rll_pol.get_roll_policy_attack(
            rollable_symbols=(sym.Blank, sym.Surge,),
        ),
        roll_limit=k,
    )


aim = get_attack_reroll(2)
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

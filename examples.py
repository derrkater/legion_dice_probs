from pprint import pprint

from legion_dice_probs import actions
from legion_dice_probs.events import count_symbols as count
from legion_dice_probs.events import aim_reroll
from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import dice_pool_with_tokens as dce_wtoks
from legion_dice_probs.stochastic_states import tokens as toks
from legion_dice_probs.stochastic_states import tokens_specialized as toks_spec


def run_examples_with_raw_dice_probabilities():
    rebel_troopers = dce.DicePool.from_dice_list(
        [
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
        ]
    )
    print('rebel troopers')
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))

    rebel_troopers_with_z6_with_trooper = dce.DicePool.from_dice_list(
        [
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
        ]
    )
    print('rebel troopers with Z6 and trooper')
    pprint(count.CountSymbols().on(rebel_troopers_with_z6_with_trooper).get_best(3))

    droid_toopers_with_gun_with_trooper = dce.DicePool.from_dice_list(
        [
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.WhiteAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
        ]
    )
    print('droid troopers')
    pprint(count.CountSymbols().on(droid_toopers_with_gun_with_trooper).get_best(3))


def run_examples_with_dice_conversion_before_calculation():
    rebel_troopers = dce.DicePool.from_dice_list(
        [
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
        ]
    )
    print('rebel troopers - before surges')
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))
    print('rebel troopers - after surge conversion')
    rebel_troopers = actions.convert_all_surges_to_hit.on(rebel_troopers)
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))
    print('rebel troopers - crits counted as hits')
    rebel_troopers = actions.convert_all_crits_to_hits_for_calculation.on(rebel_troopers)
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))


def run_examples_with_critical_and_aim__critical_applied_only_before_aim():
    rebel_troopers = dce.DicePool.from_dice_list(
        [
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
        ]
    )
    print('rebel troopers')
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))

    rebel_troopers = actions.critical_2.on(rebel_troopers)
    print('rebel troopers - after critical 2')
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))

    rebel_troopers = actions.aim.on(rebel_troopers)
    print('rebel troopers - after aim')
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))

    rebel_troopers = actions.convert_all_crits_to_hits_for_calculation.on(rebel_troopers)
    rebel_troopers = actions.remove_unconverted_surge_results_attack.on(rebel_troopers)
    print('rebel troopers - count')
    pprint(count.CountSymbols().on(rebel_troopers).get_best(10))


if __name__ == '__main__':
    # run_examples_with_raw_dice_probabilities()
    # run_examples_with_dice_conversion_before_calculation()
    # run_examples_with_critical_and_aim__critical_applied_only_before_aim()

    rebel_troopers = dce_wtoks.DicePoolWithTokens.from_dice_list_and_tokens(
        [
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            # att_dse.BlackAttackDouse(),
            # att_dse.BlackAttackDouse(),
        ],
        tokens=toks_spec.TokensAttack.from_attack_tokens(n_aim=1),
    )
    print('rebel troopers')
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))
    rebel_troopers = actions.aim.on(rebel_troopers)
    print('rebel troopers - after aim')
    pprint(rebel_troopers)
    pprint(count.CountSymbols().on(rebel_troopers).get_best(3))

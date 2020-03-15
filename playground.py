from pprint import pprint

from legion_dice_probs.events import convert_surge as conv
from legion_dice_probs.events import count_symbols as count
from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import dice_pool as dce


if __name__ == '__main__':
    rebel_troopers = dce.DicePool.from_dice_list(
        [
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
            att_dse.BlackAttackDouse(),
        ]
    )
    print('rebel troopers')
    pprint(count.CountSymbols.on(rebel_troopers))

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
    pprint(count.CountSymbols.on(rebel_troopers_with_z6_with_trooper))

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
    pprint(count.CountSymbols.on(droid_toopers_with_gun_with_trooper))

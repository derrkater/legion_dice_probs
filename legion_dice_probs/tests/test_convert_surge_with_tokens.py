from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import dice_pool_attack as dce_att
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.events import convert_surge_with_tokens as conv_srge_wtok
from legion_dice_probs.events.tools import conversion_policy as conv_pol


def test_convert_surge__on_rolled_dice_pool():
    rolled_dice_pool = dce_att.RolledDicePoolAttack.from_rolled_dice_list(
        [
            dse.RolledDouse(
                douse=att_dse.BlackAttackDouse(),
                symbol=sym.Surge(),
            ),
            dse.RolledDouse(
                douse=att_dse.RedAttackDouse(),
                symbol=sym.Hit(),
            ),
            dse.RolledDouse(
                douse=att_dse.WhiteAttackDouse(),
                symbol=sym.Crit(),
            ),
        ],
        n_surge_tokens=1,
    )
    rolled_dice_pool_target = dce_att.RolledDicePoolAttack.from_rolled_dice_list(
        [
            dse.RolledDouse(
                douse=att_dse.RedAttackDouse(),
                symbol=sym.Hit(),
            ),
            dse.RolledDouse(
                douse=att_dse.BlackAttackDouse(),
                symbol=sym.Crit(),
            ),
            dse.RolledDouse(
                douse=att_dse.WhiteAttackDouse(),
                symbol=sym.Crit(),
            ),
        ],
        n_surge_tokens=0,
    )
    action = conv_srge_wtok.ConvertSurgeWithTokens(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Surge,),
            conversion_target=sym.Crit(),
        ),
        conversion_limit=1,
    )
    assert action.on(rolled_dice_pool) == rolled_dice_pool_target

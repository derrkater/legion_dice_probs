import pytest

from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import dice_pool as dce
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
    )
    assert action.on(rolled_dice_pool) == rolled_dice_pool_target


@pytest.mark.parametrize(
    'symbols, n_surge_tokens, symbols_target, n_surge_tokens_target',
    (
            (
                    [sym.Surge(), sym.Surge(), sym.Surge(), sym.Surge()], 4,
                    [sym.Hit(), sym.Hit(), sym.Hit(), sym.Hit()], 0,
            ),
            (
                    [sym.Surge(), sym.Surge(), sym.Surge(), sym.Surge()], 3,
                    [sym.Hit(), sym.Surge(), sym.Hit(), sym.Hit()], 0,
            ),
            (
                    [sym.Surge(), sym.Surge(), sym.Hit(), sym.Hit()], 3,
                    [sym.Hit(), sym.Hit(), sym.Hit(), sym.Hit()], 1,
            ),
            (
                    [sym.Surge(), sym.Surge(), sym.Hit(), sym.Hit()], 1,
                    [sym.Hit(), sym.Hit(), sym.Surge(), sym.Hit()], 0,
            ),
    )
)
def test_convert_surge__on_rolled_dice_pool_attack__to_hit__single_dice_type(
        symbols,
        n_surge_tokens,
        symbols_target,
        n_surge_tokens_target,
):
    rolled_dice_pool = dce_att.RolledDicePoolAttack.from_rolled_dice_list(
        [
            dse.RolledDouse(
                douse=att_dse.BlackAttackDouse(),
                symbol=symbol,
            ) for symbol in symbols
        ],
        n_surge_tokens=n_surge_tokens,
    )
    rolled_dice_pool_target = dce_att.RolledDicePoolAttack.from_rolled_dice_list(
        [
            dse.RolledDouse(
                douse=att_dse.BlackAttackDouse(),
                symbol=symbol,
            ) for symbol in symbols_target
        ],
        n_surge_tokens=n_surge_tokens_target,
    )
    action = conv_srge_wtok.ConvertSurgeWithTokens(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Surge,),
            conversion_target=sym.Hit(),
        ),
    )
    assert action.on(rolled_dice_pool) == rolled_dice_pool_target


@pytest.mark.parametrize(
    'rolled_dice_list',
    (
            (
                    [
                        dse.RolledDouse(
                            douse=att_dse.WhiteAttackDouse(),
                            symbol=sym.Surge(),
                        ),
                    ]
            ),
            (
                    [
                        dse.RolledDouse(
                            douse=att_dse.WhiteAttackDouse(),
                            symbol=sym.Surge(),
                        ),
                        dse.RolledDouse(
                            douse=att_dse.WhiteAttackDouse(),
                            symbol=sym.Hit(),
                        ),
                    ]
            ),
    )
)
def test_convert_surge__on_rolled_dice_pool__no_surge_tokens(rolled_dice_list):
    rolled_dice_pool = dce.RolledDicePool.from_rolled_dice_list(rolled_dice_list)
    action = conv_srge_wtok.ConvertSurgeWithTokens(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Surge,),
            conversion_target=sym.Hit(),
        ),
        conversion_limit=None,
    )
    assert action.on(rolled_dice_pool) == rolled_dice_pool.get_probability_distribution()


@pytest.mark.parametrize(
    'dice_list',
    (
            (
                    [
                        att_dse.RedAttackDouse(),
                    ]
            ),
            (
                    [
                        att_dse.RedAttackDouse(),
                        att_dse.RedAttackDouse(),
                        att_dse.WhiteAttackDouse(),
                        att_dse.WhiteAttackDouse(),
                    ]
            ),
    )
)
def test_convert_surge__on_dice_pool__no_surge_tokens(dice_list):
    dice_pool = dce.DicePool.from_dice_list(dice_list)
    action = conv_srge_wtok.ConvertSurgeWithTokens(
        conversion_policy=conv_pol.get_conversion_policy_attack(
            convertible_symbols=(sym.Surge,),
            conversion_target=sym.Hit(),
        ),
        conversion_limit=None,
    )
    assert action.on(dice_pool) == dice_pool.get_probability_distribution()

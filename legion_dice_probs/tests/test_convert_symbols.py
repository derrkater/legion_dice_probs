import fractions

import pytest

from legion_dice_probs.events.tools import conversion_policy as conv_pol
from legion_dice_probs.events import convert_surges as conv_srge
from legion_dice_probs.events import convert_symbols as conv_syms
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms


@pytest.mark.parametrize(
    "n_converts, symbols, symbols_target",
    (
            (
                    2,
                    [
                        sym.Hit(),
                        sym.Hit(),
                        sym.Blank(),
                        sym.Surge(),
                        sym.Surge(),
                        sym.Crit(),
                    ],
                    [
                        sym.Hit(),
                        sym.Crit(),
                        sym.Crit(),
                        sym.Surge(),
                        sym.Crit(),
                        sym.Hit(),
                    ]
            ),
            (
                    1,
                    [
                        sym.Hit(),
                        sym.Hit(),
                        sym.Blank(),
                        sym.Surge(),
                        sym.Surge(),
                        sym.Crit(),
                    ],
                    [
                        sym.Hit(),
                        sym.Crit(),
                        sym.Surge(),
                        sym.Surge(),
                        sym.Crit(),
                        sym.Hit(),
                    ]
            ),
            (
                    4,
                    [
                        sym.Hit(),
                        sym.Hit(),
                        sym.Blank(),
                        sym.Surge(),
                        sym.Surge(),
                        sym.Crit(),
                    ],
                    [
                        sym.Hit(),
                        sym.Crit(),
                        sym.Crit(),
                        sym.Crit(),
                        sym.Crit(),
                        sym.Crit(),
                    ]
            )
    )
)
def test_convert_symbols__conversion_order__symbols(n_converts, symbols, symbols_target):
    conversion = conv_syms.ConvertSymbols(
        conversion_policy=conv_pol.ConversionPolicyAttackAnyToCrit(),
        conversion_limit=n_converts,
    )
    assert conversion.on(syms.Symbols.from_symbols_list(symbols)) == syms.Symbols.from_symbols_list(symbols_target)


@pytest.mark.parametrize(
    "conversion_policy, n_converts, rolled_dice, rolled_dice_target",
    (
            (
                    conv_pol.ConversionPolicyAttackAnyToCrit(),
                    2,
                    [
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Surge()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                    ],
                    [
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Crit()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Crit()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                    ]
            ),
            (
                    conv_pol.ConversionPolicyAttackAnyToCrit(),
                    1,
                    [
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Surge()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                    ],
                    [
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Crit()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Surge()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                    ]
            ),
            (
                    conv_pol.ConversionPolicyAttackAnyToCrit(),
                    3,
                    [
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Crit()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Surge()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                    ],
                    [
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Crit()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Crit()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Crit()),
                    ]
            ),
            (
                    conv_pol.ConversionPolicyAttackAnyToCrit(),
                    2,
                    [
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Surge()),
                    ],
                    [
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Crit()),
                        dse.RolledDouse(att_dse.RedAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Crit()),
                        dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Surge()),
                    ]
            ),
            (
                    conv_pol.ConversionPolicyAttackSurgeToHit(),
                    1,
                    [
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                    ],
                    [
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Blank()),
                    ],
            ),
            (
                    conv_pol.ConversionPolicyAttackSurgeToHit(),
                    1,
                    [
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Surge()),
                    ],
                    [
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Blank()),
                    ],
            ),
            (
                    conv_pol.ConversionPolicyAttackSurgeToHit(),
                    3,
                    [
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Blank()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Surge()),
                    ],
                    [
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
                        dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Blank()),
                    ],
            ),
    )
)
def test_convert_symbols__conversion_order__rolled_dice_pool(
        conversion_policy,
        n_converts,
        rolled_dice,
        rolled_dice_target,
):
    conversion = conv_syms.ConvertSymbols(
        conversion_policy=conversion_policy,
        conversion_limit=n_converts,
    )
    assert conversion.on(
        dce.RolledDicePool.from_rolled_dice_list(rolled_dice)
    ) == dce.RolledDicePool.from_rolled_dice_list(rolled_dice_target)

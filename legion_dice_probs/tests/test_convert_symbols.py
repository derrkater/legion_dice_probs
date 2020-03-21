import fractions

import pytest

import legion_dice_probs.events.tools.conversion_policy
from legion_dice_probs.events import convert_surge as conv_srge
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
        conversion_policy=legion_dice_probs.events.tools.conversion_policy.ConversionPolicyAttackAnyToCrit(),
        conversion_limit=n_converts,
    )
    assert conversion.on(syms.Symbols.from_symbols_list(symbols)) == syms.Symbols.from_symbols_list(symbols_target)


# @pytest.mark.parametrize(
#     "n_converts, symbols, symbols_target",
#     (
#             (
#                     2,
#                     [
#                         dce.RolledDicePool.from_rolled_dice_list(
#                             [
#                                 dse.RolledDouse(att_dse.RedAttackDouse(), sym.Hit()),
#                                 dse.RolledDouse(att_dse.BlackAttackDouse(), sym.Hit()),
#                                 dse.RolledDouse(att_dse.WhiteAttackDouse(), sym.Hit()),
#                             ]
#                         )
#                         sym.Hit(),
#                         sym.Hit(),
#                         sym.Blank(),
#                         sym.Surge(),
#                         sym.Surge(),
#                         sym.Crit(),
#                     ],
#                     [
#                         sym.Hit(),
#                         sym.Crit(),
#                         sym.Crit(),
#                         sym.Surge(),
#                         sym.Crit(),
#                         sym.Hit(),
#                     ]
#             ),
#             (
#                     1,
#                     [
#                         sym.Hit(),
#                         sym.Hit(),
#                         sym.Blank(),
#                         sym.Surge(),
#                         sym.Surge(),
#                         sym.Crit(),
#                     ],
#                     [
#                         sym.Hit(),
#                         sym.Crit(),
#                         sym.Surge(),
#                         sym.Surge(),
#                         sym.Crit(),
#                         sym.Hit(),
#                     ]
#             ),
#             (
#                     4,
#                     [
#                         sym.Hit(),
#                         sym.Hit(),
#                         sym.Blank(),
#                         sym.Surge(),
#                         sym.Surge(),
#                         sym.Crit(),
#                     ],
#                     [
#                         sym.Hit(),
#                         sym.Crit(),
#                         sym.Crit(),
#                         sym.Crit(),
#                         sym.Crit(),
#                         sym.Crit(),
#                     ]
#             )
#     )
# )
# def test_convert_symbols__conversion_order__rolled_dice_pool(n_converts, symbols, symbols_target):
#     conversion = conv_syms.ConvertSymbols(
#         conversion_policy=legion_dice_probs.events.tools.conversion_policy.ConversionPolicyAttackAnyToCrit(),
#         conversion_limit=n_converts,
#     )
#     assert conversion.on(syms.Symbols.from_symbols_list(symbols)) == syms.Symbols.from_symbols_list(symbols_target)

import fractions

import pytest

from legion_dice_probs import actions
from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms


def test_convert_surge__on_symbol__surge():
    symbol = sym.Surge()
    assert actions.convert_all_surges_to_block.on(symbol) == sym.Block()


def test_convert_surge__on_symbol__no_surge():
    symbol = sym.Hit()
    assert actions.convert_all_surges_to_crit.on(symbol) == symbol


def test_convert_surge__on_symbols():
    symbols = syms.Symbols.from_symbols_list(
        [
            sym.Hit(),
            sym.Surge(),
            sym.Blank(),
        ]
    )
    symbols_target = syms.Symbols.from_symbols_list(
        [
            sym.Hit(),
            sym.Crit(),
            sym.Blank(),
        ]
    )
    assert actions.convert_all_surges_to_crit.on(symbols) == symbols_target


def test_convert_surge__on_symbols__no_surge():
    symbols = syms.Symbols.from_symbols_list(
        [
            sym.Hit(),
            sym.Hit(),
            sym.Blank(),
        ]
    )
    assert actions.convert_all_surges_to_crit.on(symbols) == symbols


def test_convert_surge__on_rolled_douse__surge():
    rolled_douse = dse.RolledDouse(
        douse=att_dse.RedAttackDouse(),
        symbol=sym.Surge(),
    )
    assert actions.convert_all_surges_to_crit.on(rolled_douse).symbol == sym.Crit()


def test_convert_surge__on_rolled_douse__no_surge():
    rolled_douse = dse.RolledDouse(
        douse=att_dse.WhiteAttackDouse(),
        symbol=sym.Crit(),
    )
    assert actions.convert_all_surges_to_hit.on(rolled_douse) == rolled_douse


def test_convert_surge__on_rolled_douse__surge__wrong_conversion():
    rolled_douse = dse.RolledDouse(
        douse=att_dse.BlackAttackDouse(),
        symbol=sym.Surge(),
    )
    with pytest.raises(ValueError):
        actions.convert_all_surges_to_block.on(rolled_douse)


def test_convert_surge__on_rolled_douse__no_surge__wrong_conversion():
    # todo: test warning check.
    pass


def test_convert_surge__on_rolled_dice_pool():
    rolled_dice_pool = dce.RolledDicePool.from_rolled_dice_list(
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
        ]
    )
    rolled_dice_pool_target = dce.RolledDicePool.from_rolled_dice_list(
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
        ]
    )
    assert actions.convert_all_surges_to_crit.on(rolled_dice_pool) == rolled_dice_pool_target


def test_convert_surge__on_rolled_dice_pool__no_surge():
    rolled_dice_pool = dce.RolledDicePool.from_rolled_dice_list(
        [
            dse.RolledDouse(
                douse=att_dse.BlackAttackDouse(),
                symbol=sym.Blank(),
            ),
            dse.RolledDouse(
                douse=att_dse.RedAttackDouse(),
                symbol=sym.Hit(),
            ),
        ]
    )
    assert actions.convert_all_surges_to_crit.on(rolled_dice_pool) == rolled_dice_pool


def test_convert_surge__on_douse():
    douse = att_dse.WhiteAttackDouse()
    assert actions.convert_all_surges_to_crit.on(douse).as_dict[
               dse.RolledDouse(
                   douse=douse,
                   symbol=sym.Crit()
               )
           ] == fractions.Fraction(2, 8)
    assert actions.convert_all_surges_to_crit.on(douse).as_dict[
               dse.RolledDouse(
                   douse=douse,
                   symbol=sym.Surge()
               )
           ] == fractions.Fraction(0, 8)


def test_convert_surge__on_dice_pool():
    dice_pool = dce.DicePool.from_dice_list(
        [
            att_dse.WhiteAttackDouse(),
            att_dse.RedAttackDouse(),
            att_dse.BlackAttackDouse(),
        ]
    )
    result_all_surge = dce.RolledDicePool.from_rolled_dice_list(
        [
            dse.RolledDouse(
                douse=att_dse.WhiteAttackDouse(),
                symbol=sym.Surge()
            ),
            dse.RolledDouse(
                douse=att_dse.BlackAttackDouse(),
                symbol=sym.Surge()
            ),
            dse.RolledDouse(
                douse=att_dse.RedAttackDouse(),
                symbol=sym.Surge()
            ),
        ]
    )
    assert dice_pool.get_probability_distribution().as_dict[result_all_surge] == fractions.Fraction(
        numerator=1,
        denominator=8 ** 3,
    ), "No conversion sanity check."
    result_all_hit = dce.RolledDicePool.from_rolled_dice_list(
        [
            dse.RolledDouse(
                douse=att_dse.WhiteAttackDouse(),
                symbol=sym.Hit()
            ),
            dse.RolledDouse(
                douse=att_dse.BlackAttackDouse(),
                symbol=sym.Hit()
            ),
            dse.RolledDouse(
                douse=att_dse.RedAttackDouse(),
                symbol=sym.Hit()
            ),
        ]
    )
    assert dice_pool.get_probability_distribution().as_dict[result_all_hit] == fractions.Fraction(
        numerator=1 * 3 * 5,
        denominator=8 ** 3,
    ), "No conversion sanity check."

    dice_pool_converted_to_hit_prob_dist = actions.convert_all_surges_to_hit.on(dice_pool)
    assert dice_pool_converted_to_hit_prob_dist.as_dict[result_all_surge] == 0
    assert dice_pool_converted_to_hit_prob_dist.as_dict[result_all_hit] == fractions.Fraction(
        numerator=2 * 4 * 6,
        denominator=8 ** 3,
    )

    dice_pool_converted_to_hit_prob_dist = actions.convert_all_surges_to_crit.on(dice_pool)
    assert dice_pool_converted_to_hit_prob_dist.as_dict[result_all_surge] == 0
    assert dice_pool_converted_to_hit_prob_dist.as_dict[result_all_hit] == fractions.Fraction(
        numerator=1 * 3 * 5,
        denominator=8 ** 3,
    )

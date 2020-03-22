import fractions

import pytest

from legion_dice_probs.events import roll as rll
from legion_dice_probs.events.tools import roll_policy as rll_pol
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import defence_douse as def_dse
from legion_dice_probs.stochastic_states import symbol as sym


@pytest.mark.parametrize(
    "policy, douse_cls, symbol, target_prob_dist",
    (
            (
                    rll_pol.RollPolicyAttack(),
                    att_dse.WhiteAttackDouse,
                    sym.Blank(),
                    att_dse.WhiteAttackDouse().get_probability_distribution(),
            ),
            (
                    rll_pol.RollPolicyAttack(),
                    att_dse.BlackAttackDouse,
                    sym.Surge(),
                    att_dse.BlackAttackDouse().get_probability_distribution(),
            ),
            (
                    rll_pol.RollPolicyAttackBlanksOnly(),
                    att_dse.RedAttackDouse,
                    sym.Surge(),
                    dse.RolledDouse(att_dse.RedAttackDouse(), sym.Surge()).get_probability_distribution(),
            ),
            (
                    rll_pol.RollPolicyAttackCritFish(),
                    att_dse.RedAttackDouse,
                    sym.Hit(),
                    att_dse.RedAttackDouse().get_probability_distribution(),
            ),
    )
)
def test_roll__rolled_douse(policy, douse_cls, symbol, target_prob_dist):
    rolled_douse = dse.RolledDouse(
        douse=douse_cls(),
        symbol=symbol,
    )
    assert rll.Roll(
        roll_policy=policy,
    ).on(rolled_douse) == target_prob_dist


def test_roll__douse():
    douse = att_dse.BlackAttackDouse()
    rerolled_douse = rll.Roll(
        roll_policy=rll_pol.RollPolicyAttack()
    ).on(douse)

    crit_prob = fractions.Fraction(1, 8) * fractions.Fraction(3, 2)
    assert rerolled_douse.as_dict[
               dse.RolledDouse(
                   douse,
                   sym.Crit()
               )
           ] == crit_prob

    hit_prob = fractions.Fraction(3, 8) * fractions.Fraction(3, 2)
    assert rerolled_douse.as_dict[
               dse.RolledDouse(
                   douse,
                   sym.Hit()
               )
           ] == hit_prob

    blank_prob = fractions.Fraction(3, 8) * fractions.Fraction(1, 2)
    assert rerolled_douse.as_dict[
               dse.RolledDouse(
                   douse,
                   sym.Blank()
               )
           ] == blank_prob


def test_roll__rolled_dice_pool():
    rolled_dice_pool = dce.RolledDicePool.from_rolled_dice_list(
        [
            dse.RolledDouse(
                douse=att_dse.RedAttackDouse(),
                symbol=sym.Blank(),
            ),
            dse.RolledDouse(
                douse=att_dse.RedAttackDouse(),
                symbol=sym.Blank(),
            ),
            dse.RolledDouse(
                douse=att_dse.RedAttackDouse(),
                symbol=sym.Blank(),
            ),
        ]
    )
    aim = rll.Roll(
        roll_policy=rll_pol.RollPolicyAttack(),
        roll_limit=2,
    )
    reroll_prob_dist_dict = aim.copy().on(rolled_dice_pool).as_dict
    assert reroll_prob_dist_dict[rolled_dice_pool] == fractions.Fraction(1, 64)

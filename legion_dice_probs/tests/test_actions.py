import fractions

import pytest

from legion_dice_probs import actions
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms
from prob_dist_api import probability_distribution as pd


@pytest.mark.parametrize(
    "output, prob",
    (
            (
                    dse.RolledDouse(douse=att_dse.BlackAttackDouse(), symbol=sym.Blank()),
                    fractions.Fraction(3, 8) * fractions.Fraction(1, 2),  # 3 / 16
            ),
            (
                    dse.RolledDouse(douse=att_dse.BlackAttackDouse(), symbol=sym.Surge()),
                    fractions.Fraction(1, 8) * fractions.Fraction(1, 2),  # 1 / 16
            ),
            (
                    dse.RolledDouse(douse=att_dse.BlackAttackDouse(), symbol=sym.Hit()),
                    fractions.Fraction(3, 8) * (1 + fractions.Fraction(1, 2)),  # 9 / 16
            ),
            (
                    dse.RolledDouse(douse=att_dse.BlackAttackDouse(), symbol=sym.Crit()),
                    fractions.Fraction(1, 8) * (1 + fractions.Fraction(1, 2)),  # 3 / 16
            ),
    )
)
def test_aim__black_attack_douse(output, prob):
    douse = att_dse.BlackAttackDouse()
    rerolled_douse_prob_dist: pd.ProbabilityDistribution = actions.aim.on(douse)
    print(rerolled_douse_prob_dist)
    assert rerolled_douse_prob_dist.as_dict[output] == prob

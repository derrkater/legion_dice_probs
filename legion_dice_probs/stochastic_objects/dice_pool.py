import abc
from typing import List
import fractions
import functools
import operator

from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class DicePool(st_object.StochasticObject):
    def __init__(
            self,
            probability_distribution: pd.ProbabilityDistribution
    ):
        super().__init__(probability_distribution)

    @classmethod
    def from_dice_list(
            cls,
            dice_list: List[dse.Douse],
    ) -> "DicePool":
        if len(dice_list) == 1:
            return cls(
                probability_distribution=dice_list[0].get_probability_distribution()
            )
        else:
            dice_probability_distributions = [douse.get_probability_distribution() for douse in dice_list]
            aggregated_dice_probability_distribution = functools.reduce(
                function=operator.add,
                sequence=dice_probability_distributions,
            )
            return cls(
                probability_distribution=aggregated_dice_probability_distribution
            )


class RolledDicePool(st_state.StochasticState):
    pass

import collections
import fractions
import functools
import operator
import pprint
from typing import Counter
from typing import List

import frozendict

from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import probability_distribution as pd
from prob_dist_api import probability_distribution_utils as pd_utils
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class DicePool(st_object.StochasticObject):

    @classmethod
    def from_dice_list(
            cls,
            dice_list: List[dse.Douse],
    ) -> "DicePool":
        dice_probability_distributions = [
            douse.get_probability_distribution() for douse in dice_list
        ]
        aggregated_dice_probability_distribution = RolledDicePool.aggregate_dice_probability_distributions(
            dice_probability_distributions
        )
        return cls(
            probability_distribution=aggregated_dice_probability_distribution,
        )


class RolledDicePool(st_state.StochasticState):
    def __init__(
            self,
            rolled_dice_counter: Counter[dse.RolledDouse],
    ):
        self.rolled_dice_counter: Counter[dse.RolledDouse] = rolled_dice_counter

    def __repr__(self):
        return pprint.pformat(self.rolled_dice_counter)

    def __eq__(self, other):
        return self.rolled_dice_counter == other.rolled_dice_counter

    def __hash__(self):
        return hash(self.as_dice_frozendict)

    @property
    def as_dice_frozendict(self):
        return frozendict.frozendict(self.rolled_dice_counter)

    @classmethod
    def from_rolled_dice_list(
            cls,
            rolled_dice_list: List[dse.RolledDouse],
    ):
        return cls(collections.Counter(rolled_dice_list))

    @classmethod
    def aggregate_dice_probability_distributions(
            cls,
            probability_distributions: List[pd.ProbabilityDistribution],
    ):
        probability_distributions_of_rolled_dice_pools = [
            transform_rolled_douse_prob_dist_to_rolled_dice_pool_prob_dist(
                probability_distribution=prob_dist,
            ) for prob_dist in probability_distributions
        ]
        return functools.reduce(
            functools.partial(
                pd_utils.aggregate_probability_distributions,
                aggregate_function=operator.add,
            ),
            probability_distributions_of_rolled_dice_pools,
        )

    def __add__(self, other):
        if isinstance(other, dse.RolledDouse):
            new_rolled_dice_pool = self.copy()
            new_rolled_dice_pool.append_rolled_douse(other)
            return new_rolled_dice_pool
        elif isinstance(other, RolledDicePool):
            if type(other) == RolledDicePool:
                return self.from_rolled_dice_list(
                    list(self.rolled_dice_counter.elements()) +
                    list(other.rolled_dice_counter.elements())
                )
            else:
                return other.__radd__(self)
        else:
            return TypeError(f'unsupported operand type(s) for +: {type(self)} and {type(other)}')

    def __radd__(self, other):
        return self.__add__(other)

    def append_rolled_douse(self, douse: dse.RolledDouse) -> None:
        self.rolled_dice_counter[douse] += 1

    def copy(self) -> "RolledDicePool":
        return self.__class__(
            rolled_dice_counter=collections.Counter(self.rolled_dice_counter)
        )


def transform_rolled_douse_prob_dist_to_rolled_dice_pool_prob_dist(
        probability_distribution: pd.ProbabilityDistribution,
        rolled_dice_pool_cls: type(RolledDicePool) = RolledDicePool,
):
    prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
    for stochastic_state, prob in probability_distribution.as_dict.items():
        if isinstance(stochastic_state, dse.RolledDouse):
            prob_dist_after[
                rolled_dice_pool_cls.from_rolled_dice_list([stochastic_state])
            ] += prob
        else:
            prob_dist_after[stochastic_state] += prob

    return pd.ProbabilityDistribution(prob_dist_after)

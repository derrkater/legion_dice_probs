import collections
import fractions
import functools
import operator
import pprint
from typing import Counter
from typing import List
from typing import Union

import frozendict

from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import probability_distribution as pd
from prob_dist_api import probability_distribution_utils as pd_utils
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class DicePool(st_object.StochasticObject):

    @classmethod
    def from_douse(
            cls,
            douse: dse.Douse,
    ) -> "DicePool":
        return cls(
            probability_distribution=transform_rolled_douse_prob_dist_to_rolled_dice_pool_prob_dist(
                probability_distribution=douse.get_probability_distribution(),
            ),
        )

    @classmethod
    def from_dice_list(
            cls,
            dice_list: List[dse.Douse],
    ) -> "DicePool":
        if len(dice_list) == 1:
            return cls.from_douse(dice_list[0])
        dice_probability_distributions = [
            cls.from_douse(douse).get_probability_distribution() for douse in dice_list
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
            return self.from_rolled_dice_list(
                list(self.rolled_dice_counter.elements()) + [other]
            )
        elif isinstance(other, RolledDicePool):
            return self.from_rolled_dice_list(
                list(self.rolled_dice_counter.elements()) +
                list(other.rolled_dice_counter.elements())
            )
        else:
            return TypeError(f'unsupported operand type(s) for +: {type(self)} and {type(other)}')

    def __radd__(self, other):
        return self.__add__(other)

    @classmethod
    def aggregate_rolled_dice(
            cls,
            rolled_dice_obj_1: Union[dse.RolledDouse, "RolledDicePool"],
            rolled_dice_obj_2: Union[dse.RolledDouse, "RolledDicePool"],
    ) -> "RolledDicePool":
        if isinstance(rolled_dice_obj_1, dse.RolledDouse) and isinstance(rolled_dice_obj_2, dse.RolledDouse):
            return cls.from_rolled_dice_list(
                [
                    rolled_dice_obj_1,
                    rolled_dice_obj_2,
                ]
            )
        if isinstance(rolled_dice_obj_1, cls) and isinstance(rolled_dice_obj_2, cls):
            return cls.from_rolled_dice_list(
                list(rolled_dice_obj_1.rolled_dice_counter.elements()) +
                list(rolled_dice_obj_2.rolled_dice_counter.elements())
            )
        if isinstance(rolled_dice_obj_1, cls) and isinstance(rolled_dice_obj_2, dse.RolledDouse):
            return cls.from_rolled_dice_list(
                list(rolled_dice_obj_1.rolled_dice_counter.elements()) + [rolled_dice_obj_2]
            )
        if isinstance(rolled_dice_obj_2, cls) and isinstance(rolled_dice_obj_1, dse.RolledDouse):
            return cls.aggregate_rolled_dice(
                rolled_dice_obj_2,
                rolled_dice_obj_1
            )
        raise ValueError


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

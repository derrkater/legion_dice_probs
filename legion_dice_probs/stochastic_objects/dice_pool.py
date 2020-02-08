import collections
import functools
import operator
from typing import Counter
from typing import List

import frozendict

from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import probability_distribution as pd
from prob_dist_api import probability_distribution_utils as pd_utils
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class DicePool(st_object.StochasticObject):
    def __init__(
            self,
            probability_distribution: pd.ProbabilityDistribution,
            dice_list: List[dse.Douse],
    ):
        super().__init__(probability_distribution)
        self.dice_list: List[dse.Douse] = dice_list

    def __eq__(self, other):
        return self.as_dice_counter == other.as_dice_counter

    def __hash__(self):
        return hash(self.as_dice_frozendict) + hash(self.get_probability_distribution())

    @classmethod
    def from_dice_list(
            cls,
            dice_list: List[dse.Douse],
    ) -> "DicePool":
        if len(dice_list) == 1:
            return cls(
                probability_distribution=dice_list[0].get_probability_distribution(),
                dice_list=dice_list,
            )
        else:
            dice_probability_distributions = [douse.get_probability_distribution() for douse in dice_list]
            aggregated_dice_probability_distribution = functools.reduce(
                functools.partial(
                    pd_utils.aggregate_probability_distributions,
                    # aggregate_function=legion_st_object_utils.aggregate_rolled_douse_into_rolled_dice_pool
                ),
                dice_probability_distributions,
            )
            return cls(
                probability_distribution=aggregated_dice_probability_distribution,
                dice_list=dice_list,
            )

    @property
    def as_dice_counter(self):
        return collections.Counter(self.dice_list)

    @property
    def as_dice_frozendict(self):
        return frozendict.frozendict(self.as_dice_counter)

    def add_douse(self, douse: dse.Douse) -> None:
        self.dice_list.append(douse)


class RolledDicePool(st_state.StochasticState):
    def __init__(
            self,
            rolled_dice_counter: Counter[dse.RolledDouse],
    ):
        self.rolled_dice_counter: Counter[dse.RolledDouse] = rolled_dice_counter

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    @classmethod
    def from_rolled_dice_list(
            cls,
            rolled_dice_list: List[dse.RolledDouse],
    ):
        return cls(collections.Counter(rolled_dice_list))

    @property
    def get_symbols_counter(self) -> Counter[sym.Symbol]:
        return collections.Counter(
            mapping={
                rolled_douse.symbol: count for rolled_douse, count in self.rolled_dice_counter.items()
            }
        )

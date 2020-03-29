import collections
import functools
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
            # TODO: this probably doesn't work right as it retuns pd on douse not rolled_dice_pool.
            return cls(
                probability_distribution=dice_list[0].get_probability_distribution(),
                dice_list=dice_list,
            )
        else:
            dice_probability_distributions = [douse.get_probability_distribution() for douse in dice_list]
            aggregated_dice_probability_distribution = RolledDicePool.aggregate_dice_probability_distributions(
                dice_probability_distributions
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

    @classmethod
    def aggregate_dice(
            cls,
            dice_obj_1: Union[dse.Douse, "DicePool"],
            dice_obj_2: Union[dse.Douse, "DicePool"],
    ) -> "DicePool":
        if isinstance(dice_obj_1, dse.Douse) and isinstance(dice_obj_2, dse.Douse):
            return cls.from_dice_list(
                [
                    dice_obj_1,
                    dice_obj_2
                ]
            )
        if isinstance(dice_obj_1, cls) and isinstance(dice_obj_2, cls):
            return cls(
                probability_distribution=pd_utils.aggregate_probability_distributions(
                    pd_1=dice_obj_1.get_probability_distribution(),
                    pd_2=dice_obj_2.get_probability_distribution(),
                    aggregate_function=NotImplemented
                ),
                dice_list=dice_obj_1.dice_list + dice_obj_2.dice_list,
            )
        if isinstance(dice_obj_1, cls) and isinstance(dice_obj_2, dse.Douse):
            raise NotImplementedError
        if isinstance(dice_obj_2, cls) and isinstance(dice_obj_1, dse.Douse):
            raise NotImplementedError
        raise ValueError


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
        return functools.reduce(
            functools.partial(
                pd_utils.aggregate_probability_distributions,
                aggregate_function=cls.aggregate_rolled_dice
            ),
            probability_distributions,
        )

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

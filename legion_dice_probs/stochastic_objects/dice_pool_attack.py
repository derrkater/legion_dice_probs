import collections
import functools
from typing import Counter
from typing import List
from typing import Union

import frozendict

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import probability_distribution as pd
from prob_dist_api import probability_distribution_utils as pd_utils


class DicePoolAttack(dce.DicePool):
    @classmethod
    def from_dice_list_and_attack_tokens(
            cls,
            dice_list: List[dse.Douse],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ) -> "DicePoolAttack":
        dice_probability_distributions = [douse.get_probability_distribution() for douse in dice_list]
        aggregated_dice_probability_distribution = RolledDicePoolAttack.aggregate_dice_probability_distributions(
            dice_probability_distributions,
            n_surge_tokens=n_surge_tokens,
            n_aim_tokens=n_aim_tokens,
        )
        return cls(
            probability_distribution=aggregated_dice_probability_distribution,
            dice_list=dice_list,
        )


class RolledDicePoolAttack(dce.RolledDicePool):
    def __init__(
            self,
            rolled_dice_counter: Counter[dse.RolledDouse],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ):
        super().__init__(rolled_dice_counter)
        self.n_aim_tokens = n_aim_tokens
        self.n_surge_tokens = n_surge_tokens

    def __repr__(self):
        return f'surge:{self.n_surge_tokens},aim:{self.n_aim_tokens},{super().__repr__()}'

    def __eq__(self, other):
        return (
                super().__eq__(other) and
                self.n_surge_tokens == other.n_surge_tokens and
                self.n_aim_tokens == other.n_aim_tokens
        )

    def __hash__(self):
        return super().__hash__() + hash(self.n_aim_tokens) + hash(self.n_surge_tokens)

    @classmethod
    def from_rolled_dice_list(
            cls,
            rolled_dice_list: List[dse.RolledDouse],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ) -> "RolledDicePoolAttack":
        return cls(
            rolled_dice_counter=super().from_rolled_dice_list(rolled_dice_list).rolled_dice_counter,
            n_surge_tokens=n_surge_tokens,
            n_aim_tokens=n_aim_tokens,
        )

    @classmethod
    def aggregate_dice_probability_distributions(
            cls,
            probability_distributions: List[pd.ProbabilityDistribution],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ):
        return functools.reduce(
            functools.partial(
                pd_utils.aggregate_probability_distributions,
                aggregate_function=functools.partial(
                    cls.aggregate_rolled_dice,
                    n_surge_tokens=n_surge_tokens,
                    n_aim_tokens=n_aim_tokens,
                )
            ),
            probability_distributions,
        )

    @classmethod
    def aggregate_rolled_dice(
            cls,
            rolled_dice_obj_1: Union[dse.RolledDouse, "RolledDicePoolAttack"],
            rolled_dice_obj_2: Union[dse.RolledDouse, "RolledDicePoolAttack"],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ) -> Union[
        "RolledDicePoolAttack",
        dce.RolledDicePool,
    ]:
        if isinstance(rolled_dice_obj_1, dse.RolledDouse) and isinstance(rolled_dice_obj_2, dse.RolledDouse):
            return cls.from_rolled_dice_list(
                [
                    rolled_dice_obj_1,
                    rolled_dice_obj_2,
                ],
                n_surge_tokens=n_surge_tokens,
                n_aim_tokens=n_aim_tokens,
            )
        if isinstance(rolled_dice_obj_1, cls) and isinstance(rolled_dice_obj_2, cls):
            return cls.from_rolled_dice_list(
                list(rolled_dice_obj_1.rolled_dice_counter.elements()) +
                list(rolled_dice_obj_2.rolled_dice_counter.elements()),
                n_surge_tokens=rolled_dice_obj_1.n_surge_tokens + rolled_dice_obj_2.n_surge_tokens + n_surge_tokens,
                n_aim_tokens=rolled_dice_obj_1.n_aim_tokens + rolled_dice_obj_2.n_aim_tokens + n_aim_tokens,
            )
        if isinstance(rolled_dice_obj_1, cls) and isinstance(rolled_dice_obj_2, dse.RolledDouse):
            return cls.from_rolled_dice_list(
                list(rolled_dice_obj_1.rolled_dice_counter.elements()) + [rolled_dice_obj_2],
                n_surge_tokens=rolled_dice_obj_1.n_surge_tokens + n_surge_tokens,
                n_aim_tokens=rolled_dice_obj_1.n_aim_tokens + n_aim_tokens,
            )
        if isinstance(rolled_dice_obj_2, cls) and isinstance(rolled_dice_obj_1, dse.RolledDouse):
            return cls.aggregate_rolled_dice(
                rolled_dice_obj_2,
                rolled_dice_obj_1,
                n_surge_tokens=n_surge_tokens,
                n_aim_tokens=n_aim_tokens,
            )
        return super().aggregate_rolled_dice(rolled_dice_obj_1, rolled_dice_obj_2)

import logging
from typing import Union

from legion_dice_probs.events.tools import roll_policy as roll_pol
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import event as ev
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object


class Roll(ev.Event):

    def __init__(
            self,
            roll_policy: roll_pol.RollPolicy,
            roll_limit: int = None,
    ):
        if roll_limit is not None and roll_limit < 1:
            raise ValueError(f'Requested {roll_limit} rolls.')

        self.roll_policy = roll_policy
        self._roll_limit = roll_limit
        self._n_rolled = 0

    @property
    def roll_limit(self):
        return self._roll_limit

    @property
    def n_rolled(self):
        return self._n_rolled

    @property
    def can_roll(self):
        return self.roll_limit is None or self.n_rolled < self.roll_limit

    def mark_roll(self):
        if not self.can_roll:
            logging.warning(f'Marking roll with {self}, while roll limit of {self.roll_limit}')
        self._n_rolled += 1

    def copy(self) -> "Roll":
        return self.__class__(
            roll_policy=self.roll_policy,
            roll_limit=self.roll_limit,
        )

    def on(
            self,
            object_: Union[
                dse.RolledDouse,
                dce.RolledDicePool,
                st_object.StochasticObject,
                pd.ProbabilityDistribution,
            ]
    ) -> Union[
        pd.ProbabilityDistribution,
    ]:
        if isinstance(object_, dse.RolledDouse):
            if self.roll_policy.is_rollable(object_):
                self.mark_roll()
                return object_.douse.get_probability_distribution()
            else:
                return object_.get_probability_distribution()

        if isinstance(object_, dce.RolledDicePool):
            rolled_dice_sorted = sorted(
                object_.rolled_dice_counter.elements(),
                key=self.roll_policy.get_douse_roll_priority,
            )
            prob_dists_after = []
            for rolled_douse in rolled_dice_sorted:
                rerolled_prob_dist = self.on(rolled_douse) if self.can_roll else \
                    rolled_douse.get_probability_distribution()
                prob_dists_after.append(rerolled_prob_dist)

            # TODO: rethink if this logic should be implemented either as part of DicePool.from_dice_list or
            #  RolledDicePool.aggregate_rolled_dice. Former would extend signature with RolledDouse and latter with
            #  Douse
            aggregated_dice_probability_distribution = object_.aggregate_dice_probability_distributions(
                prob_dists_after
            )

            return aggregated_dice_probability_distribution

        return super().on(object_)

import collections
import fractions
import logging
from typing import Union

from legion_dice_probs.events.tools import roll_policy as roll_pol
from legion_dice_probs.stochastic_objects import dice_pool as dce_pool
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
                dce_pool.RolledDicePool,
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

        if isinstance(object_, dce_pool.RolledDicePool):
            raise NotImplementedError

        if isinstance(object_, st_object.StochasticObject):
            prob_dist = object_.get_probability_distribution()
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in prob_dist.as_dict.items():
                for state_after, prob_after in self.copy().on(state).as_dict.items():
                    prob_dist_after[state_after] += prob * prob_after

            return pd.ProbabilityDistribution(prob_dist_after)

        if isinstance(object_, pd.ProbabilityDistribution):
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in object_.as_dict.items():
                for state_after, prob_after in self.copy().on(state).as_dict.items():
                    prob_dist_after[state_after] += prob * prob_after

            return pd.ProbabilityDistribution(prob_dist_after)

        raise NotImplementedError(f'{type(object_)} is not supported.')

import logging
from typing import Union

from legion_dice_probs.probability_distributions import douse_probability_distribution as dse_pd
from legion_dice_probs.stochastic_objects import dice_pool as dce_pool
from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import event as ev
from prob_dist_api import probability_distribution as pd


class Roll(ev.Event):

    def __init__(
            self,
            n_dice: int = 1,
    ):
        self.n_dice: int = n_dice

    def on(
            self,
            object_: Union[
                dse.Douse,
                dce_pool.DicePool,
                dse_pd.DouseProbabilityDistribution,
            ]
    ) -> Union[
        pd.ProbabilityDistribution,
    ]:
        if isinstance(object_, dse.Douse):
            if self.n_dice != 1:
                logging.warning(f'Trying to roll {self.n_dice} dice when {object_} is given.')
            return object_.get_probability_distribution()
        elif isinstance(object_, dce_pool.DicePool):
            raise NotImplementedError


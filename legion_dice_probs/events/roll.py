from typing import Union

from legion_dice_probs.probability_distributions import douse_probability_distribution as dse_pd
from legion_dice_probs.stochastic_objects import dice_pool as dce_pool
from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import event as ev


class Roll(ev.Event):

    def on(
            self,
            object_: Union[
                dse.Douse,
                dce_pool.DicePool,
                dse_pd.DouseProbabilityDistribution,
            ]
    ) -> Union[
        dse_pd.DouseProbabilityDistribution,
    ]:
        raise NotImplementedError

from typing import Union

from prob_dist_api import event
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class ConvertSurge(event.Event):
    def on(self, object_: Union[
        st_state.StochasticState,
        st_object.StochasticObject,
        pd.ProbabilityDistribution,
    ]) -> pd.ProbabilityDistribution:
        raise NotImplementedError
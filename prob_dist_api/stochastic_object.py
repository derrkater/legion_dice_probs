import abc
from typing import List

from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_state as st_state


class StochasticObject(abc.ABC):

    def __init__(
            self,
            probability_distribution: pd.ProbabilityDistribution,
    ):
        self._probability_distribution = probability_distribution

    def get_probability_distribution(self) -> pd.ProbabilityDistribution:
        return self._probability_distribution

    def get_stochastic_states(self) -> List[st_state.StochasticState]:
        return list(self.get_probability_distribution().as_dict.keys())

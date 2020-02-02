import abc
from typing import List

from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_state as st_state


class StochasticObject(abc.ABC):

    @abc.abstractmethod
    def get_probability_distribution(self) -> pd.ProbabilityDistribution:
        raise NotImplementedError

    def get_stochastic_states(self) -> List[st_state.StochasticState]:
        return list(self.get_probability_distribution().as_dict.keys())

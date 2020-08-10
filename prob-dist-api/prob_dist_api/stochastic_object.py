import abc
from typing import Hashable
from typing import List

from prob_dist_api import probability_distribution as pd


# TODO: remove stochastic object as unnecessary wrapper of probability distribution which can be fully defined by it's
#  Stochastic states
class StochasticObject(abc.ABC):

    def __init__(
            self,
            probability_distribution: pd.ProbabilityDistribution,
    ):
        self._probability_distribution = probability_distribution

    def get_probability_distribution(self) -> pd.ProbabilityDistribution:
        return self._probability_distribution

    def get_stochastic_states(self) -> List[Hashable]:
        return list(self.get_probability_distribution().as_dict.keys())

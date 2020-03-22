import abc
from typing import Union

from prob_dist_api import stochastic_state as st_state
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import probability_distribution as pd


class Event(abc.ABC):

    @abc.abstractmethod
    def on(
            self,
            object_: Union[
                st_state.StochasticState,
                st_object.StochasticObject,
                pd.ProbabilityDistribution,
            ],
    ) -> pd.ProbabilityDistribution:
        raise NotImplementedError

    @abc.abstractmethod
    @property
    def is_used(self) -> bool:
        raise NotImplementedError

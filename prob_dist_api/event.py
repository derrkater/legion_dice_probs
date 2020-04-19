import collections
import fractions
from abc import abstractmethod
from typing import Union

from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class Event:

    @abstractmethod
    def copy(self) -> "Event":
        raise NotImplementedError

    def on(
            self,
            object_: Union[
                st_state.StochasticState,
                st_object.StochasticObject,
                pd.ProbabilityDistribution,
            ],
    ) -> pd.ProbabilityDistribution:

        if isinstance(object_, st_object.StochasticObject):
            prob_dist = object_.get_probability_distribution()
            return self.on(prob_dist)

        if isinstance(object_, pd.ProbabilityDistribution):
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in object_.as_dict.items():
                state_after_event = self.copy().on(state)
                if isinstance(state_after_event, pd.ProbabilityDistribution):
                    for state_after, prob_after in state_after_event.as_dict.items():
                        prob_dist_after[state_after] += prob * prob_after
                else:
                    prob_dist_after[state_after_event] += prob

            return pd.ProbabilityDistribution(prob_dist_after)

        raise NotImplementedError(f'{type(object_)} is not supported.')

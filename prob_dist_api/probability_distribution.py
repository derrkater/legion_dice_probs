import collections
import fractions
import operator
from typing import Callable
from typing import Counter
from typing import DefaultDict
from typing import Dict
from typing import List

from prob_dist_api import stochastic_state as st_state


class ProbabilityDistribution:

    def __init__(
            self,
            probability_distribution_dict: Dict[st_state.StochasticState, fractions.Fraction],
    ):
        if sum(probability_distribution_dict.values()) != 1.:
            raise ProbabilityNotEqualOne

        self._dict: Dict[st_state.StochasticState, fractions.Fraction] = probability_distribution_dict

    @property
    def as_dict(self) -> Dict[st_state.StochasticState, fractions.Fraction]:
        return self._dict

    @classmethod
    def from_events_counter(
            cls,
            events_counter: Counter[st_state.StochasticState, int],
    ):
        probability_distribution_dict = {}

        total = sum(events_counter.values())
        for state, count in events_counter.items():
            if events_counter[state] < 0:
                raise NegativeProbabilityError
            probability_distribution_dict[state] = fractions.Fraction(
                probability_distribution_dict[state],
                total
            )

        return cls(probability_distribution_dict)

    @classmethod
    def from_events_list(
            cls,
            events_list: List[st_state.StochasticState],
    ) -> "ProbabilityDistribution":
        return cls(collections.Counter(events_list))


class ProbabilityNotEqualOne(ValueError):
    pass


class NegativeProbabilityError(ValueError):
    pass


def aggregate_probability_distributions(
        pd_1: ProbabilityDistribution,
        pd_2: ProbabilityDistribution,
        aggregate_function: Callable[
            [st_state.StochasticState, ...],
            st_state.StochasticState
        ] = operator.add,
) -> ProbabilityDistribution:
    aggregated_pd_dict: DefaultDict[
        st_state.StochasticState,
        fractions.Fraction
    ] = collections.defaultdict(lambda: fractions.Fraction(0))

    for state_1, prob_1 in pd_1.as_dict.items():
        for state_2, prob_2 in pd_2.as_dict.items():
            aggregated_state = aggregate_function(state_1, state_2)
            aggregated_pd_dict[aggregated_state] += prob_1 * prob_2

    return ProbabilityDistribution(aggregated_pd_dict)

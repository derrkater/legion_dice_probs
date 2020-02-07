import collections
import fractions
import operator
from typing import Callable, DefaultDict

from prob_dist_api import stochastic_state as st_state
from prob_dist_api.probability_distribution import ProbabilityDistribution


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

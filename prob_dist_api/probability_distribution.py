from typing import Dict, Counter, List
import collections
import fractions

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

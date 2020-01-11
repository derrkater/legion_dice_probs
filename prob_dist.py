import collections
import fractions
from copy import deepcopy
from typing import Counter, List

import utils


class NegativeProbabilityError(ValueError):
    pass


class StochasticState:
    def __init__(self, prob_dist: "ProbDist"):
        self._prob_dist = prob_dist

    @property
    def prob_dist(self):
        return deepcopy(self._prob_dist)


class ProbDist(collections.Counter):
    """
    Discrete finite probability distribution.

    from: http://practicallypredictable.com/2017/12/04/probability-distributions-dice-rolls/
    """

    def __init__(self, mapping: Counter[StochasticState], **kwargs):
        super().__init__()
        self._counter: Counter[StochasticState] = mapping
        self.update(mapping, **kwargs)
        total = sum(self.values())
        for event in self:
            if self[event] < 0:
                raise NegativeProbabilityError
            self[event] = fractions.Fraction(self[event], total)

    @classmethod
    def from_events_list(cls, states_list: List[StochasticState]):
        return cls(collections.Counter(states_list))

    @property
    def aggregation_class(self):
        return ProbDist

    @property
    def values_product_function(self):
        return lambda x, y: x * y

    @property
    def keys_merge_function(self):
        return lambda x, y: x + y

    def __add__(self, other):
        # return ProbDist(it.product(self.events_list, other.events_list))
        return self.aggregation_class(
            utils.get_counters_product_mapping(
                counter_1=self._counter,
                counter_2=other._counter,
                product_function=self.values_product_function,
                key_merge_function=self.keys_merge_function
            )
        )

import collections
import fractions
from typing import Counter

import utils


class NegativeProbabilityError(ValueError):
    pass


class ProbDist(collections.Counter):
    """
    Discrete finite probability distribution.

    from: http://practicallypredictable.com/2017/12/04/probability-distributions-dice-rolls/
    """

    def __init__(self, mapping: Counter, **kwargs):
        super().__init__()
        self._counter = mapping
        self.update(mapping, **kwargs)
        total = sum(self.values())
        for event in self:
            if self[event] < 0:
                raise NegativeProbabilityError
            self[event] = fractions.Fraction(self[event], total)

    @classmethod
    def from_events_list(cls, events_list):
        return cls(collections.Counter(events_list))

    @property
    def events_list(self):
        return self._events_list

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

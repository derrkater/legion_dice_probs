import collections
import fractions
from typing import List


class NegativeProbabilityError(ValueError):
    pass


class ProbDist(collections.Counter):
    """
    Discrete finite probability distribution.

    from: http://practicallypredictable.com/2017/12/04/probability-distributions-dice-rolls/
    """

    def __init__(self, events_list: List, **kwargs):
        super().__init__()
        self._events_list = events_list
        self.update(collections.Counter(events_list), **kwargs)
        total = sum(self.values())
        for event in self:
            if self[event] < 0:
                raise NegativeProbabilityError
            self[event] = fractions.Fraction(self[event], total)

    @property
    def events_list(self):
        return self._events_list

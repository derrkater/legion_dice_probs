import collections
import fractions
import pprint
from typing import Counter
from typing import Dict
from typing import Hashable
from typing import List

import frozendict


class ProbabilityDistribution:

    def __init__(
            self,
            probability_distribution_dict: Dict[Hashable, fractions.Fraction],
    ):
        if sum(probability_distribution_dict.values()) != 1.:
            raise ProbabilityNotEqualOne

        self._dict: Dict[Hashable, fractions.Fraction] = probability_distribution_dict

    def __repr__(self):
        return pprint.pformat(self.as_dict)

    def __eq__(self, other):
        return self.as_dict == other.as_dict

    def __hash__(self):
        return hash(self.as_frozendict)

    @property
    def as_dict(self) -> Dict[Hashable, fractions.Fraction]:
        return self._dict

    @property
    def as_frozendict(self):
        return frozendict.frozendict(self.as_dict)

    @classmethod
    def from_events_counter(
            cls,
            events_counter: Counter[Hashable],
    ):
        probability_distribution_dict = {}

        total = sum(events_counter.values())
        for state, count in events_counter.items():
            if events_counter[state] < 0:
                raise NegativeProbabilityError
            probability_distribution_dict[state] = fractions.Fraction(
                count,
                total
            )

        return cls(probability_distribution_dict)

    @classmethod
    def from_events_list(
            cls,
            events_list: List[Hashable],
    ) -> "ProbabilityDistribution":
        return cls.from_events_counter(collections.Counter(events_list))


class ProbabilityNotEqualOne(ValueError):
    pass


class NegativeProbabilityError(ValueError):
    pass

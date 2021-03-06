import collections
import fractions
import operator
import pprint
from typing import Counter
from typing import Dict
from typing import Hashable
from typing import List

import frozendict


# todo: implement percentage output.
class ProbabilityDistribution:

    def __init__(
            self,
            probability_distribution_dict: Dict[Hashable, fractions.Fraction],
    ):
        if sum(probability_distribution_dict.values()) != 1.:
            raise ProbabilityNotEqualOne

        self._dict: Dict[Hashable, fractions.Fraction] = probability_distribution_dict

    def __repr__(self):
        return pprint.pformat(self.as_dict_with_floats)

    def __eq__(self, other):
        return self.as_dict == other.as_dict

    def __hash__(self):
        return hash(self.as_frozendict)

    @property
    def as_dict(self) -> Dict[Hashable, fractions.Fraction]:
        return self._dict

    @property
    def as_dict_with_floats(self) -> Dict[Hashable, float]:
        return {
            key: float(val) for key, val in self.as_dict.items()
        }

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

    def get_best(
            self,
            n: int = 1,
            as_float: bool = True,
    ):
        dict_items = self.as_dict_with_floats.items() if as_float else self.as_dict.items()
        return sorted(
            dict_items,
            key=operator.itemgetter(1),
            reverse=True,
        )[:n]


class ProbabilityNotEqualOne(ValueError):
    pass


class NegativeProbabilityError(ValueError):
    pass

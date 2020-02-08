from abc import ABC

import dice
import prob_dist as pd


class DicePool(pd.ProbDist, ABC):
    @property
    def aggregation_class(self):
        return self.__class__

    @property
    def keys_merge_function(self):
        return lambda x, y: dice.RollResult([x, y])

    def __add__(self, other):
        if issubclass(other.__class__, dice.Douse) or issubclass(other.__class__, DicePool):
            return super().__add__(other)
        else:
            raise NotImplementedError

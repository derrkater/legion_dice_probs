from abc import ABC

import dice
import prob_dist
import roll_results


class DiceNumberNegativeError(ValueError):
    pass


class DicePoolEmptyError(ValueError):
    pass


class DicePool(prob_dist.ProbDist, ABC):
    @property
    def aggregation_class(self):
        return self.__class__

    @property
    def keys_merge_function(self):
        return lambda x, y: roll_results.RollResult([x, y])

    def __add__(self, other):
        if issubclass(other.__class__, dice.Douse) or issubclass(other.__class__, DicePool):
            return super().__add__(other)
        else:
            raise NotImplementedError

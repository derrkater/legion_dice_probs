import collections
import fractions


class NegativeProbabilityError(ValueError):
    pass


class ProbDist(collections.Counter):
    """
    Discrete finite probability distribution.

    from: http://practicallypredictable.com/2017/12/04/probability-distributions-dice-rolls/
    """

    def __init__(self, mapping=(), **kwargs):
        super().__init__()
        self.update(mapping, **kwargs)
        total = sum(self.values())
        for event in self:
            if self[event] < 0:
                raise NegativeProbabilityError
            self[event] = fractions.Fraction(self[event], total)

import abc
import fractions
from collections import Hashable

from prob_dist_api import probability_distribution as pd


class StochasticState(abc.ABC, Hashable):
    def get_probability_distribution(self) -> pd.ProbabilityDistribution:
        return pd.ProbabilityDistribution(
            {
                self: fractions.Fraction(1)
            }
        )

    @abc.abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self):
        raise NotImplementedError

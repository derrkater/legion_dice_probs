import abc
from typing import List

from legion_dice_probs.stochastic_states import symbol as sym
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class Douse(st_object.StochasticObject, abc.ABC):
    def __init__(self):
        super().__init__(self.get_default_probability_distribution())

    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return hash(type(self))

    def __repr__(self):
        return type(self).__name__

    def get_default_probability_distribution(self) -> pd.ProbabilityDistribution:
        return pd.ProbabilityDistribution.from_events_list(
            [
                RolledDouse(
                    self,
                    side,
                ) for side in self.get_sides()
            ]
        )

    @abc.abstractmethod
    def get_sides(self) -> List[sym.Symbol]:
        raise NotImplementedError


class RolledDouse(st_state.StochasticState):
    def __init__(
            self,
            douse: Douse,
            symbol: sym.Symbol,
    ):
        self.douse: Douse = douse
        self.symbol: sym.Symbol = symbol

    def __eq__(self, other):
        return (
                self.symbol == other.symbol and
                self.douse == other.douse
        )

    def __hash__(self):
        return hash(self.symbol) + hash(self.douse)

    def __repr__(self):
        return f'{self.douse}({self.symbol})'

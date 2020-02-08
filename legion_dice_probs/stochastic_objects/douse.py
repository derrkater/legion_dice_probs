import abc
from typing import List
from typing import Optional

from legion_dice_probs.stochastic_states import symbol as sym
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class Douse(st_object.StochasticObject, abc.ABC):
    def __init__(
            self,
            probability_distribution: Optional[pd.ProbabilityDistribution] = None,
    ):
        super().__init__(
            probability_distribution or self.get_default_probability_distribution()
        )

    def __eq__(self, other):
        return (
                type(self).__name__ == type(other).__name__ and
                self.get_probability_distribution() == other.get_probability_distribution()
        )

    def __hash__(self):
        return hash(type(self).__name__) + hash(self.get_probability_distribution())

    def __repr__(self):
        return type(self).__name__

    def get_default_probability_distribution(self) -> pd.ProbabilityDistribution:
        return pd.ProbabilityDistribution.from_events_list(
            [
                self.get_rolled_douse_cls()(
                    self,
                    side,
                ) for side in self.get_sides()
            ]
        )

    @abc.abstractmethod
    def get_sides(self) -> List[sym.Symbol]:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_rolled_douse_cls() -> "RolledDouse".__class__:
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
        return True
        # return (
        #         self.symbol == other.symbol and
        #         self.douse == other.douse
        # )

    def __hash__(self):
        return hash(self.symbol) + hash(type(self.douse).__name__)
        # return hash(self.symbol) + hash(self.douse)

    def __repr__(self):
        return f'{self.douse}({self.symbol})'

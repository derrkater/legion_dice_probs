import abc
from typing import List
from typing import Optional

from legion_dice_probs.probability_distributions import douse_probability_distribution as dse_pd
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

    def get_default_probability_distribution(self) -> dse_pd.DouseProbabilityDistribution:
        return dse_pd.DouseProbabilityDistribution.from_events_list(
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
    def get_rolled_douse_cls() -> "RolledDouse".__class__:
        return RolledDouse


class RolledDouse(st_state.StochasticState):
    def __init__(
            self,
            douse: Douse,
            symbol: sym.Symbol,
    ):
        self.douse: Douse = douse
        self.symbol: sym.Symbol = symbol

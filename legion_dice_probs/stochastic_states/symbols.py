from typing import List

from legion_dice_probs.stochastic_states import symbol as sym
from prob_dist_api import stochastic_state as st_state


class Symbols(st_state.StochasticState):

    def __init__(
            self,
            symbols: List[sym.Symbol],
    ):
        self._symbols: List[sym.Symbol] = symbols

    @property
    def symbols(self) -> List[sym.Symbol]:
        return self._symbols

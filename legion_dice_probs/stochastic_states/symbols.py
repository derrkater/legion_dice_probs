import collections
from typing import Counter
from typing import List

import frozendict as frozendict

from legion_dice_probs.stochastic_states import symbol as sym
from prob_dist_api import stochastic_state as st_state


class Symbols(st_state.StochasticState):

    def __init__(
            self,
            symbols_counter: Counter[sym.Symbol],
    ):
        self._symbols_counter: Counter[sym.Symbol] = symbols_counter

    @property
    def symbols_list(self) -> List[sym.Symbol]:
        return list(self._symbols_counter.elements())

    @property
    def symbols_counter(self) -> Counter[sym.Symbol]:
        return self._symbols_counter

    @property
    def as_frozendict(self) -> frozendict.frozendict:
        return frozendict.frozendict(self.symbols_counter)

    def __eq__(self, other):
        return self.symbols_counter == other.symbols_counter

    def __hash__(self):
        return hash(self.as_frozendict)

    @classmethod
    def from_symbols_list(
            cls,
            symbols_list: List[sym.Symbol],
    ):
        return cls(collections.Counter(symbols_list))

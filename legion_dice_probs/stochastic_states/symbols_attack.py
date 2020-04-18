import collections
from typing import Counter
from typing import List

import frozendict as frozendict

from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms


class SymbolsAttack(syms.Symbols):

    def __init__(
            self,
            symbols_counter: Counter[sym.Symbol],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ):
        super().__init__(symbols_counter)
        self.n_aim_tokens = n_aim_tokens
        self.n_surge_tokens = n_surge_tokens

    @property
    def symbols_list(self) -> List[sym.Symbol]:
        return list(self._symbols_counter.elements())

    @property
    def symbols_counter(self) -> Counter[sym.Symbol]:
        return self._symbols_counter

    @property
    def as_frozendict(self) -> frozendict.frozendict:
        return frozendict.frozendict(self.symbols_counter)

    def __repr__(self):
        return f'surge:{self.n_surge_tokens},aim:{self.n_aim_tokens},{super().__repr__()}'

    def __eq__(self, other):
        return (
                super().__eq__(other) and
                self.n_surge_tokens == other.n_surge_tokens and
                self.n_aim_tokens == other.n_aim_tokens
        )

    def __hash__(self):
        return super().__hash__() + hash(self.n_aim_tokens) + hash(self.n_surge_tokens)

    @classmethod
    def from_symbols_list(
            cls,
            symbols_list: List[sym.Symbol],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ):
        return cls(
            symbols_counter=collections.Counter(symbols_list),
            n_surge_tokens=n_surge_tokens,
            n_aim_tokens=n_aim_tokens,
        )

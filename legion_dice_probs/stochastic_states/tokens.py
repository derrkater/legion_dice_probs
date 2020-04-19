import collections
import pprint
from typing import Counter
from typing import List

import frozendict as frozendict

from legion_dice_probs.stochastic_states import token as tok
from prob_dist_api import stochastic_state as st_state


# TODO: this is virtually the same as Symbols. Refactor into one object?
class Tokens(st_state.StochasticState):

    def __init__(
            self,
            tokens_counter: Counter[tok.Token],
    ):
        self._tokens_counter: Counter[tok.Token] = tokens_counter

    @property
    def tokens_list(self) -> List[tok.Token]:
        return list(self._tokens_counter.elements())

    @property
    def tokens_counter(self) -> Counter[tok.Token]:
        return self._tokens_counter

    @property
    def as_frozendict(self) -> frozendict.frozendict:
        return frozendict.frozendict(self.tokens_counter)

    def __repr__(self):
        return pprint.pformat(self.tokens_counter)

    def __eq__(self, other):
        return self.tokens_counter == other.tokens_counter

    def __hash__(self):
        return hash(self.as_frozendict)

    @classmethod
    def from_symbols_list(
            cls,
            symbols_list: List[tok.Token],
    ):
        return cls(collections.Counter(symbols_list))

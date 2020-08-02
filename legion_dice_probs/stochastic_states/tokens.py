import collections
import pprint
from typing import Counter
from typing import List
from typing import Optional

import frozendict as frozendict

from legion_dice_probs.stochastic_states import token as tok
from prob_dist_api import stochastic_state as st_state


# TODO: this is virtually the same as Symbols. Refactor into one object?
class Tokens(st_state.StochasticState):

    def __init__(
            self,
            tokens_counter: Optional[Counter[tok.Token]] = None,
    ):
        self._tokens_counter: Counter[tok.Token] = tokens_counter or collections.Counter([])

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

    def __len__(self):
        return len(self.tokens_list)

    def __add__(self, other):
        return self.__class__(self.tokens_counter + other.tokens_counter)

    @classmethod
    def from_tokens_list(
            cls,
            tokens_list: List[tok.Token],
    ):
        return cls(collections.Counter(tokens_list))

    def copy(self):
        return self.__class__(collections.Counter(self.tokens_counter))

    def remove_token(self, token: tok.Token):
        if self.tokens_counter[token] == 0:
            raise KeyError(f'There are not tokens: {token} in {self}.')
        self.tokens_counter[token] -= 1

    def count_tokens(self, token: tok.Token) -> int:
        return self.tokens_counter[token]

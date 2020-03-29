import collections
from typing import Counter
from typing import List

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse


class RolledDicePoolAttack(dce.RolledDicePool):
    def __init__(
            self,
            rolled_dice_counter: Counter[dse.RolledDouse],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ):
        super().__init__(rolled_dice_counter)
        self.n_aim_tokens = n_aim_tokens
        self.n_surge_tokens = n_surge_tokens

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
    def from_rolled_dice_list(
            cls,
            rolled_dice_list: List[dse.RolledDouse],
            n_surge_tokens: int = 0,
            n_aim_tokens: int = 0,
    ):
        return cls(
            rolled_dice_counter=super().from_rolled_dice_list(rolled_dice_list).rolled_dice_counter,
            n_surge_tokens=n_surge_tokens,
            n_aim_tokens=n_aim_tokens,
        )

import collections
from abc import ABC
from typing import List

import dice_pool
import dice_symbols as sym
import prob_dist
import roll_results


class Douse(prob_dist.ProbDist, ABC):
    def __init__(self, **kwargs):
        super().__init__(
            collections.Counter(self.events_list),
            **kwargs
        )

    @property
    def aggregation_class(self):
        return dice_pool.DicePool

    @property
    def keys_merge_function(self):
        return lambda x, y: roll_results.RollResult([x, y])

    def __add__(self, other):
        if issubclass(type(other), Douse) or issubclass(type(other), dice_pool.DicePool):
            return super().__add__(other)
        else:
            super().__add__(other)


class AttackDouse(Douse, ABC):
    pass


class RedAttackDouse(AttackDouse):

    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Crit(),
            sym.Surge(),
            sym.Hit(),
            sym.Hit(),
            sym.Hit(),
            sym.Hit(),
            sym.Hit(),
            sym.Blank(),
        ]


class BlackAttackDouse(AttackDouse):
    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Crit(),
            sym.Surge(),
            sym.Hit(),
            sym.Hit(),
            sym.Hit(),
            sym.Blank(),
            sym.Blank(),
            sym.Blank(),
        ]


class WhiteAttackDouse(AttackDouse):
    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Crit(),
            sym.Surge(),
            sym.Hit(),
            sym.Blank(),
            sym.Blank(),
            sym.Blank(),
            sym.Blank(),
            sym.Blank(),
        ]


class DefenceDouse(Douse, ABC):
    pass


class RedDefenceDouse(DefenceDouse):
    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Surge(),
            sym.Block(),
            sym.Block(),
            sym.Block(),
            sym.Blank(),
            sym.Blank(),
        ]


class WhiteDefenceDouse(DefenceDouse):
    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Surge(),
            sym.Block(),
            sym.Blank(),
            sym.Blank(),
            sym.Blank(),
            sym.Blank(),
        ]

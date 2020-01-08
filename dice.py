import collections
from abc import ABC
from typing import List

import dice_colors as col
import dice_pool
import dice_symbols as sym
import prob_dist
import roll_result


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
        return lambda x, y: roll_result.RollResult([x, y])

    def __add__(self, other):
        if issubclass(type(other), Douse) or issubclass(type(other), dice_pool.DicePool):
            return super().__add__(other)
        else:
            super().__add__(other)


class AttackDouse(Douse, ABC):
    pass


class RedAttackDouse(AttackDouse):
    color = col.Red()

    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Crit(self.color),
            sym.Surge(self.color),
            sym.Hit(self.color),
            sym.Hit(self.color),
            sym.Hit(self.color),
            sym.Hit(self.color),
            sym.Hit(self.color),
            sym.Blank(self.color),
        ]


class BlackAttackDouse(AttackDouse):
    color = col.Black()

    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Crit(self.color),
            sym.Surge(self.color),
            sym.Hit(self.color),
            sym.Hit(self.color),
            sym.Hit(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
        ]


class WhiteAttackDouse(AttackDouse):
    color = col.White()

    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Crit(self.color),
            sym.Surge(self.color),
            sym.Hit(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
        ]


class DefenceDouse(Douse, ABC):
    pass


class RedDefenceDouse(DefenceDouse):
    color = col.Red()

    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Surge(self.color),
            sym.Block(self.color),
            sym.Block(self.color),
            sym.Block(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
        ]


class WhiteDefenceDouse(DefenceDouse):
    color = col.White()

    @property
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Surge(self.color),
            sym.Block(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
            sym.Blank(self.color),
        ]

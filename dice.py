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
    def color(self):
        raise NotImplementedError

    @property
    def _symbols_list(self) -> List[type(sym.Symbol)]:
        raise NotImplementedError

    @property
    def events_list(self) -> List[sym.Symbol]:
        return [symbol_cls(self) for symbol_cls in self._symbols_list]

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
    @property
    def color(self):
        return col.Red()

    @property
    def _symbols_list(self) -> List[type(sym.Symbol)]:
        return [
            sym.Crit,
            sym.Surge,
            sym.Hit,
            sym.Hit,
            sym.Hit,
            sym.Hit,
            sym.Hit,
            sym.Blank,
        ]


class BlackAttackDouse(AttackDouse):
    @property
    def color(self):
        return col.Black()

    @property
    def _symbols_list(self) -> List[type(sym.Symbol)]:
        return [
            sym.Crit,
            sym.Surge,
            sym.Hit,
            sym.Hit,
            sym.Hit,
            sym.Blank,
            sym.Blank,
            sym.Blank,
        ]


class WhiteAttackDouse(AttackDouse):
    @property
    def color(self):
        return col.White()

    @property
    def _symbols_list(self) -> List[type(sym.Symbol)]:
        return [
            sym.Crit,
            sym.Surge,
            sym.Hit,
            sym.Blank,
            sym.Blank,
            sym.Blank,
            sym.Blank,
            sym.Blank,
        ]


class DefenceDouse(Douse, ABC):
    pass


class RedDefenceDouse(DefenceDouse):
    @property
    def color(self):
        return col.Red()

    @property
    def _symbols_list(self) -> List[type(sym.Symbol)]:
        return [
            sym.Surge,
            sym.Block,
            sym.Block,
            sym.Block,
            sym.Blank,
            sym.Blank,
        ]


class WhiteDefenceDouse(DefenceDouse):
    @property
    def color(self):
        return col.White()

    @property
    def _symbols_list(self) -> List[type(sym.Symbol)]:
        return [
            sym.Surge,
            sym.Block,
            sym.Blank,
            sym.Blank,
            sym.Blank,
            sym.Blank,
        ]

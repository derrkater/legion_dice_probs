from abc import ABC
from typing import List

import dice_symbols as sym
import prob_dist


class Douse(prob_dist.ProbDist, ABC):
    def __init__(self, **kwargs):
        super().__init__(self.events_list, **kwargs)


class AttackDouse(Douse, ABC):
    pass


class RedAttackDouse(AttackDouse):

    @property
    def events_list(self) -> List[sym.Symbol]:
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
    def events_list(self) -> List[sym.Symbol]:
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
    def events_list(self) -> List[sym.Symbol]:
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
    def events_list(self) -> List[sym.Symbol]:
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
    def events_list(self) -> List[sym.Symbol]:
        return [
            sym.Surge,
            sym.Block,
            sym.Blank,
            sym.Blank,
            sym.Blank,
            sym.Blank,
        ]

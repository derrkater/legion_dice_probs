import collections
from abc import ABC, abstractmethod
from typing import List

import dice_symbols as sym
import prob_dist


class Douse(prob_dist.ProbDist, ABC):
    def __init__(self, mapping=None, **kwargs):
        mapping = mapping or collections.Counter(self.get_sides())
        super().__init__(mapping, **kwargs)

    @classmethod
    def get_prob_dist(cls):
        return prob_dist.ProbDist(mapping=collections.Counter(cls.get_sides()))

    @classmethod
    @abstractmethod
    def get_sides(cls) -> List[sym.Symbol]:
        raise NotImplementedError


class AttackDouse(Douse, ABC):
    pass


class RedAttackDouse(AttackDouse):
    @classmethod
    def get_sides(cls) -> List[sym.Symbol]:
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
    @classmethod
    def get_sides(cls) -> List[sym.Symbol]:
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
    @classmethod
    def get_sides(cls) -> List[sym.Symbol]:
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
    raise NotImplementedError


class RedDefenceDouse(DefenceDouse):
    raise NotImplementedError


class WhiteDefenceDouse(DefenceDouse):
    raise NotImplementedError

import abc
from typing import List

from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym


class AttackDouse(dse.Douse, abc.ABC):
    pass


class RedAttackDouse(AttackDouse):

    def get_sides(self) -> List[sym.Symbol]:
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

    def get_sides(self) -> List[sym.Symbol]:
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

    def get_sides(self) -> List[sym.Symbol]:
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

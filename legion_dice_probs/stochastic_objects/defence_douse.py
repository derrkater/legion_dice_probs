import abc
from typing import List

from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym


class DefenceDouse(dse.Douse, abc.ABC):
    pass


class RedDefenceDouse(DefenceDouse):

    def get_sides(self) -> List[sym.Symbol]:
        return [
            sym.Block(),
            sym.Block(),
            sym.Block(),
            sym.Surge(),
            sym.Blank(),
            sym.Blank(),
        ]


class WhiteDefenceDouse(DefenceDouse):

    def get_sides(self) -> List[sym.Symbol]:
        return [
            sym.Block(),
            sym.Surge(),
            sym.Blank(),
            sym.Blank(),
            sym.Blank(),
            sym.Blank(),
        ]

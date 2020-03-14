from typing import List

from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym


class Sym1(sym.Symbol):
    pass


class Sym2(sym.Symbol):
    pass


class Douse1(dse.Douse):

    def get_sides(self) -> List[sym.Symbol]:
        return [
            Sym1(),
            Sym1(),
            Sym2(),
        ]

    @staticmethod
    def get_rolled_douse_cls() -> type(dse.RolledDouse):
        return RolledDouse1


class RolledDouse1(dse.RolledDouse):
    pass


class Douse2(dse.Douse):

    def get_sides(self) -> List[sym.Symbol]:
        return [
            Sym1(),
            Sym2(),
            Sym2(),
        ]

    @staticmethod
    def get_rolled_douse_cls() -> type(dse.RolledDouse):
        return RolledDouse2


class RolledDouse2(dse.RolledDouse):
    pass

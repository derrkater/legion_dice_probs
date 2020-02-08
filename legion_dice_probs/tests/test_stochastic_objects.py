import collections
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
        return dse.RolledDouse


class Douse2(dse.Douse):

    def get_sides(self) -> List[sym.Symbol]:
        return [
            Sym1(),
            Sym2(),
            Sym2(),
        ]

    @staticmethod
    def get_rolled_douse_cls() -> type(dse.RolledDouse):
        return dse.RolledDouse


def test_douse__should_implement_equal():
    assert Douse1() == Douse1()
    assert Douse1() != Douse2()


def test_douse__should_implement_hash():
    assert len(
        collections.Counter(
            [
                Douse1(),
                Douse1(),
                Douse2(),
            ]
        )
    ) == 2

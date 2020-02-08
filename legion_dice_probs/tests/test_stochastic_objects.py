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


def test_rolled_douse__should_implement_equal():
    rolled_douse_1_sym_1 = RolledDouse1(
        douse=Douse1(),
        symbol=Sym1(),
    )
    rolled_douse_1_sym_2 = RolledDouse1(
        douse=Douse1(),
        symbol=Sym2(),
    )
    rolled_douse_2_sym_1 = RolledDouse2(
        douse=Douse2(),
        symbol=Sym1(),
    )
    rolled_douse_2_sym_2 = RolledDouse2(
        douse=Douse2(),
        symbol=Sym2(),
    )
    assert rolled_douse_1_sym_1 == RolledDouse1(
        douse=Douse1(),
        symbol=Sym1(),
    )
    assert rolled_douse_2_sym_2 == RolledDouse2(
        douse=Douse2(),
        symbol=Sym2(),
    )
    assert rolled_douse_1_sym_1 != rolled_douse_1_sym_2
    assert rolled_douse_1_sym_1 != rolled_douse_2_sym_1


def test_rolled_douse__should_implement_hash():
    assert len(
        collections.Counter(
            [
                RolledDouse1(
                    douse=Douse1(),
                    symbol=Sym1(),
                ),
                RolledDouse1(
                    douse=Douse1(),
                    symbol=Sym1(),
                ),
                RolledDouse1(
                    douse=Douse1(),
                    symbol=Sym2(),
                ),
                RolledDouse2(
                    douse=Douse2(),
                    symbol=Sym1(),
                ),
            ]
        )
    ) == 3

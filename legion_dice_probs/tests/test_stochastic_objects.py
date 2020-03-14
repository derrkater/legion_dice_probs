import collections
import fractions
from typing import List

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_objects import utils as legion_st_objects_utils
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


def test_aggregate_rolled_dice__2_dice_same():
    rolled_dice = legion_st_objects_utils.aggregate_rolled_dice(
        RolledDouse1(
            douse=Douse1(),
            symbol=Sym1(),
        ),
        RolledDouse1(
            douse=Douse1(),
            symbol=Sym1(),
        ),
    )
    assert len(rolled_dice.rolled_dice_counter) == 1


def test_aggregate_rolled_dice__2_dice_different():
    rolled_dice = legion_st_objects_utils.aggregate_rolled_dice(
        RolledDouse1(
            douse=Douse1(),
            symbol=Sym1(),
        ),
        RolledDouse1(
            douse=Douse1(),
            symbol=Sym2(),
        ),
    )
    assert len(rolled_dice.rolled_dice_counter) == 2


def test_aggregate_rolled_dice__dice_pool_and_same_douse():
    appended_douse = RolledDouse1(
        douse=Douse1(),
        symbol=Sym2(),
    )
    rolled_dice = legion_st_objects_utils.aggregate_rolled_dice(
        dce.RolledDicePool(
            rolled_dice_counter=collections.Counter(
                [
                    RolledDouse1(
                        douse=Douse1(),
                        symbol=Sym1(),
                    ),
                    RolledDouse1(
                        douse=Douse1(),
                        symbol=Sym2(),
                    ),
                ]
            )
        ),
        appended_douse,
    )
    assert len(rolled_dice.rolled_dice_counter) == 2
    assert rolled_dice.rolled_dice_counter[appended_douse] == 2


def test_aggregate_rolled_dice__dice_pool_and_new_douse():
    appended_douse = RolledDouse1(
        douse=Douse2(),
        symbol=Sym2(),
    )
    rolled_dice = legion_st_objects_utils.aggregate_rolled_dice(
        dce.RolledDicePool(
            rolled_dice_counter=collections.Counter(
                [
                    RolledDouse1(
                        douse=Douse1(),
                        symbol=Sym1(),
                    ),
                    RolledDouse1(
                        douse=Douse1(),
                        symbol=Sym2(),
                    ),
                ]
            )
        ),
        appended_douse,
    )
    assert len(rolled_dice.rolled_dice_counter) == 3
    assert rolled_dice.rolled_dice_counter[appended_douse] == 1


def test_aggregate_rolled_dice__dice_pools():
    rolled_dice_pool_1 = dce.RolledDicePool(
        rolled_dice_counter=collections.Counter(
            [
                RolledDouse1(
                    douse=Douse1(),
                    symbol=Sym1(),
                ),
                RolledDouse1(
                    douse=Douse1(),
                    symbol=Sym2(),
                ),
            ]
        )
    )
    rolled_dice_pool_2 = dce.RolledDicePool(
        rolled_dice_counter=collections.Counter(
            [
                RolledDouse1(
                    douse=Douse2(),
                    symbol=Sym1(),
                ),
                RolledDouse1(
                    douse=Douse1(),
                    symbol=Sym2(),
                ),
            ]
        )
    )
    rolled_dice = legion_st_objects_utils.aggregate_rolled_dice(
        rolled_dice_pool_1,
        rolled_dice_pool_2,
    )
    assert len(rolled_dice.rolled_dice_counter) == 3


def test_dice_pool__should_be_created_from_list():
    dice_list = [
        Douse1(),
        Douse1(),
        Douse2(),
    ]
    dice_pool = dce.DicePool.from_dice_list(dice_list)
    assert dice_pool.dice_list == dice_list
    assert dice_pool.get_probability_distribution().as_dict[
               dce.RolledDicePool.from_rolled_dice_list(
                   rolled_dice_list=[
                       RolledDouse1(
                           douse=Douse1(),
                           symbol=Sym1(),
                       ),
                       RolledDouse1(
                           douse=Douse1(),
                           symbol=Sym1(),
                       ),
                       RolledDouse2(
                           douse=Douse2(),
                           symbol=Sym1(),
                       )
                   ]
               )
           ] == fractions.Fraction(4, 27), 'Proper probability calculation'
    assert dice_pool.as_dice_counter[Douse2()] == 1

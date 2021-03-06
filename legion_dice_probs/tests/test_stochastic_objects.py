import collections
import fractions

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.tests.stubs import Douse1, Douse2, Sym1, Sym2


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
    rolled_douse_1_sym_1 = dse.RolledDouse(
        douse=Douse1(),
        symbol=Sym1(),
    )
    rolled_douse_1_sym_2 = dse.RolledDouse(
        douse=Douse1(),
        symbol=Sym2(),
    )
    rolled_douse_2_sym_1 = dse.RolledDouse(
        douse=Douse2(),
        symbol=Sym1(),
    )
    rolled_douse_2_sym_2 = dse.RolledDouse(
        douse=Douse2(),
        symbol=Sym2(),
    )
    assert rolled_douse_1_sym_1 == dse.RolledDouse(
        douse=Douse1(),
        symbol=Sym1(),
    )
    assert rolled_douse_2_sym_2 == dse.RolledDouse(
        douse=Douse2(),
        symbol=Sym2(),
    )
    assert rolled_douse_1_sym_1 != rolled_douse_1_sym_2
    assert rolled_douse_1_sym_1 != rolled_douse_2_sym_1


def test_rolled_douse__should_implement_hash():
    assert len(
        collections.Counter(
            [
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym1(),
                ),
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym1(),
                ),
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym2(),
                ),
                dse.RolledDouse(
                    douse=Douse2(),
                    symbol=Sym1(),
                ),
            ]
        )
    ) == 3


# def test_aggregate_rolled_dice__2_dice_same():
#     rolled_dice = dce.RolledDicePool.aggregate_rolled_dice(
#         dse.RolledDouse(
#             douse=Douse1(),
#             symbol=Sym1(),
#         ),
#         dse.RolledDouse(
#             douse=Douse1(),
#             symbol=Sym1(),
#         ),
#     )
#     assert len(rolled_dice.rolled_dice_counter) == 1


# def test_aggregate_rolled_dice__2_dice_different():
#     rolled_dice = dce.RolledDicePool.aggregate_rolled_dice(
#         dse.RolledDouse(
#             douse=Douse1(),
#             symbol=Sym1(),
#         ),
#         dse.RolledDouse(
#             douse=Douse1(),
#             symbol=Sym2(),
#         ),
#     )
#     assert len(rolled_dice.rolled_dice_counter) == 2


def test_add_rolled_dice_pool__dice_pool_and_same_douse():
    appended_douse = dse.RolledDouse(
        douse=Douse1(),
        symbol=Sym2(),
    )
    rolled_dice = dce.RolledDicePool(
        rolled_dice_counter=collections.Counter(
            [
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym1(),
                ),
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym2(),
                ),
            ]
        )
    ) + appended_douse
    assert len(rolled_dice.rolled_dice_counter) == 2
    assert rolled_dice.rolled_dice_counter[appended_douse] == 2


def test_add_rolled_dice_pool__dice_pool_and_new_douse():
    appended_douse = dse.RolledDouse(
        douse=Douse2(),
        symbol=Sym2(),
    )
    rolled_dice = dce.RolledDicePool(
        rolled_dice_counter=collections.Counter(
            [
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym1(),
                ),
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym2(),
                ),
            ]
        )
    ) + appended_douse
    assert len(rolled_dice.rolled_dice_counter) == 3
    assert rolled_dice.rolled_dice_counter[appended_douse] == 1


def test_add_rolled_dice_pool__dice_pools():
    rolled_dice_pool_1 = dce.RolledDicePool(
        rolled_dice_counter=collections.Counter(
            [
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym1(),
                ),
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym2(),
                ),
            ]
        )
    )
    rolled_dice_pool_2 = dce.RolledDicePool(
        rolled_dice_counter=collections.Counter(
            [
                dse.RolledDouse(
                    douse=Douse2(),
                    symbol=Sym1(),
                ),
                dse.RolledDouse(
                    douse=Douse1(),
                    symbol=Sym2(),
                ),
            ]
        )
    )
    rolled_dice = rolled_dice_pool_1 + rolled_dice_pool_2
    assert len(rolled_dice.rolled_dice_counter) == 3


def test_dice_pool__should_be_created_from_list():
    dice_list = [
        Douse1(),
        Douse1(),
        Douse2(),
    ]
    dice_pool = dce.DicePool.from_dice_list(dice_list)
    assert dice_pool.get_probability_distribution().as_dict[
               dce.RolledDicePool.from_rolled_dice_list(
                   rolled_dice_list=[
                       dse.RolledDouse(
                           douse=Douse1(),
                           symbol=Sym1(),
                       ),
                       dse.RolledDouse(
                           douse=Douse1(),
                           symbol=Sym1(),
                       ),
                       dse.RolledDouse(
                           douse=Douse2(),
                           symbol=Sym1(),
                       )
                   ]
               )
           ] == fractions.Fraction(4, 27), 'Proper probability calculation'

import fractions

from legion_dice_probs.events.count_symbols import CountSymbols
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_states import symbols as syms
from legion_dice_probs.tests.stubs import Douse1, Douse2, Sym1, Sym2, RolledDouse1, RolledDouse2


def test_count_single_symbol():
    symbol = Sym1()
    assert CountSymbols.on(symbol) == syms.Symbols.from_symbols_list([Sym1()])


def test_count_symbols():
    symbols = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym1(),
            Sym2(),
        ]
    )
    assert symbols == CountSymbols.on(symbols)


def test_count_single_rolled_douse():
    rolled_douse = RolledDouse1(
        douse=Douse1(),
        symbol=Sym1(),
    )
    assert CountSymbols.on(rolled_douse) == syms.Symbols.from_symbols_list([Sym1()])


def test_count_rolled_dice():
    rolled_dice_pool = dce.RolledDicePool.from_rolled_dice_list(
        [
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
            )
        ]
    )
    symbols = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym1(),
            Sym2(),
        ]
    )
    assert CountSymbols.on(rolled_dice_pool) == symbols


def test_count_single_douse():
    douse = Douse1()
    symbols = syms.Symbols.from_symbols_list(
        [
            Sym1(),
        ]
    )
    assert CountSymbols.on(douse).as_dict[symbols] == fractions.Fraction(2, 3)


def test_count_dice_pool():
    dice_pool = dce.DicePool.from_dice_list(
        [
            Douse1(),
            Douse1(),
            Douse2(),
        ]
    )
    symbols = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym1(),
            Sym1(),
        ]
    )
    assert CountSymbols.on(dice_pool).as_dict[symbols] == fractions.Fraction(4, 27)

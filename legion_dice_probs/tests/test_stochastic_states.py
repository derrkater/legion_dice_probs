from collections import Counter

from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms


class Symbol1(sym.Symbol):
    pass


class Symbol2(sym.Symbol):
    pass


def test_symbol__should_implement_equality():
    assert Symbol1() == Symbol1()
    assert Symbol1() != Symbol2()


def test_symbol__should_implement_hash():
    assert len(
        Counter([
            Symbol1(),
            Symbol1(),
            Symbol2(),
        ])
    ) == 2


def test_symbols__should_be_created_from_symbols_list():
    symbols = syms.Symbols.from_symbols_list(
        [
            Symbol1(),
            Symbol1(),
            Symbol2(),
        ]
    )
    assert len(symbols.symbols_counter) == 2
    assert len(symbols.symbols_list) == 3


def test_symbols__should_implement_equality():
    symbols_1 = syms.Symbols.from_symbols_list(
        [
            Symbol1(),
            Symbol1(),
            Symbol2(),
        ]
    )
    symbols_2 = syms.Symbols.from_symbols_list(
        [
            Symbol1(),
            Symbol2(),
            Symbol1(),
        ]
    )
    symbols_3 = syms.Symbols.from_symbols_list(
        [
            Symbol1(),
            Symbol2(),
            Symbol2(),
        ]
    )

    assert symbols_1 == symbols_2
    assert symbols_1 != symbols_3


def test_symbols__should_implement_hashable():
    symbols_1 = syms.Symbols.from_symbols_list(
        [
            Symbol1(),
            Symbol1(),
            Symbol2(),
        ]
    )
    symbols_2 = syms.Symbols.from_symbols_list(
        [
            Symbol1(),
            Symbol2(),
            Symbol1(),
        ]
    )
    symbols_3 = syms.Symbols.from_symbols_list(
        [
            Symbol1(),
            Symbol2(),
            Symbol2(),
        ]
    )

    assert len(
        Counter(
            [
                symbols_1,
                symbols_2,
                symbols_3,
            ]
        )
    ) == 2
    assert hash(symbols_1) == hash(symbols_2)

from collections import Counter

import pytest

from legion_dice_probs.stochastic_states import symbols as syms
from legion_dice_probs.stochastic_states import tokens as toks
from legion_dice_probs.tests.stubs import Sym1, Sym2, Tok1, Tok2


def test_symbol__should_implement_equality():
    assert Sym1() == Sym1()
    assert Sym1() != Sym2()


def test_symbol__should_implement_hash():
    assert len(
        Counter([
            Sym1(),
            Sym1(),
            Sym2(),
        ])
    ) == 2


def test_symbols__should_be_created_from_symbols_list():
    symbols = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym1(),
            Sym2(),
        ]
    )
    assert len(symbols.symbols_counter) == 2
    assert len(symbols.symbols_list) == 3


def test_symbols__should_implement_equality():
    symbols_1 = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym1(),
            Sym2(),
        ]
    )
    symbols_2 = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym2(),
            Sym1(),
        ]
    )
    symbols_3 = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym2(),
            Sym2(),
        ]
    )

    assert symbols_1 == symbols_2
    assert symbols_1 != symbols_3


def test_symbols__should_implement_hashable():
    symbols_1 = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym1(),
            Sym2(),
        ]
    )
    symbols_2 = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym2(),
            Sym1(),
        ]
    )
    symbols_3 = syms.Symbols.from_symbols_list(
        [
            Sym1(),
            Sym2(),
            Sym2(),
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


def test_tokens__count_tokens__zero_case():
    tokens = toks.Tokens.from_tokens_list([])
    assert tokens.count_tokens(Tok2()) == 0


def test_tokens__count_tokens():
    tokens = toks.Tokens.from_tokens_list(
        [
            Tok1(),
            Tok1(),
            Tok2(),
        ]
    )
    assert tokens.count_tokens(Tok1()) == 2
    assert tokens.count_tokens(Tok2()) == 1


def test_tokens__remove_token():
    tokens = toks.Tokens.from_tokens_list(
        [
            Tok1(),
            Tok1(),
        ]
    )
    tokens.remove_token(Tok1())
    assert tokens.count_tokens(Tok1()) == 1


def test_tokens__remove_token__no_target_token():
    tokens = toks.Tokens.from_tokens_list(
        [
            Tok1(),
            Tok1(),
        ]
    )
    with pytest.raises(KeyError):
        tokens.remove_token(Tok2())

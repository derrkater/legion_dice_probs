from collections import Counter

import pytest

from legion_dice_probs.stochastic_states import symbol as sym


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

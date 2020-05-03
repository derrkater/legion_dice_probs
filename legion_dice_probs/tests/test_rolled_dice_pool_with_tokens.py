import collections

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import dice_pool_with_tokens as dce_toks
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import token as tok
from legion_dice_probs.stochastic_states import tokens as toks
from legion_dice_probs.tests.stubs import Douse1, Douse2, Sym1, Sym2


def test_add_rolled_dice_pool__dice_pool_and_dice_pool_with_tokens():
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
    rolled_dice_pool_2 = dce_toks.RolledDicePoolWithTokens(
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
        ),
        tokens=toks.Tokens.from_tokens_list(
            [
                tok.Token(),
                tok.Token(),
            ]
        )
    )
    rolled_dice = rolled_dice_pool_1 + rolled_dice_pool_2
    assert len(rolled_dice.rolled_dice_counter) == 3
    assert len(rolled_dice.tokens) == 2

    rolled_dice = rolled_dice_pool_2 + rolled_dice_pool_1
    assert len(rolled_dice.tokens) == 2

    rolled_dice = rolled_dice_pool_2 + rolled_dice_pool_2
    assert len(rolled_dice.tokens) == 4

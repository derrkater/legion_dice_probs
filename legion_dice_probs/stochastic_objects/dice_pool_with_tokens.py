import collections
from typing import Counter
from typing import List
from typing import Optional

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import tokens as toks


class DicePoolWithTokens(dce.DicePool):

    @classmethod
    def from_dice_list_and_tokens(
            cls,
            dice_list: List[dse.Douse],
            tokens: toks.Tokens,
    ) -> "DicePoolWithTokens":
        dice_pool = super().from_dice_list(dice_list)
        probability_distribution = {
            RolledDicePoolWithTokens.from_rolled_dice_pool(
                rolled_dice_pool=rolled_dice_pool,
                tokens=tokens.copy(),
            )
            for rolled_dice_pool, prob in dice_pool.get_probability_distribution().as_dict.items()
        }
        return cls(probability_distribution)


class RolledDicePoolWithTokens(dce.RolledDicePool):

    def __init__(
            self,
            rolled_dice_counter: Counter[dse.RolledDouse],
            tokens: Optional[toks.Tokens] = None,
    ):
        super().__init__(rolled_dice_counter)
        self.tokens = tokens or toks.Tokens()

    def __repr__(self):
        return self.tokens.__repr__() + super().__repr__()

    def __eq__(self, other):
        return (
                self.tokens == other.tokens and
                super().__eq__(other)
        )

    def __hash__(self):
        return super().__hash__() + hash(self.tokens)

    @classmethod
    def from_rolled_dice_list_and_tokens(
            cls,
            rolled_dice_list: List[dse.RolledDouse],
            tokens: toks.Tokens,
    ):
        return cls(
            rolled_dice_counter=collections.Counter(rolled_dice_list),
            tokens=tokens,
        )

    @classmethod
    def from_rolled_dice_pool(
            cls,
            rolled_dice_pool: dce.RolledDicePool,
            tokens: toks.Tokens,
    ):
        return cls(
            rolled_dice_counter=collections.Counter(rolled_dice_pool.rolled_dice_counter),
            tokens=tokens,
        )

    def __add__(self, other):
        if isinstance(other, RolledDicePoolWithTokens):
            tokens = self.tokens + other.tokens
            rolled_dice_list = list(self.rolled_dice_counter.elements()) + list(other.rolled_dice_counter.elements())
            return self.from_rolled_dice_list_and_tokens(
                rolled_dice_list=rolled_dice_list,
                tokens=tokens,
            )
        if isinstance(other, dce.RolledDicePool):
            rolled_dice_list = list(self.rolled_dice_counter.elements()) + list(other.rolled_dice_counter.elements())
            return self.from_rolled_dice_list_and_tokens(
                rolled_dice_list=rolled_dice_list,
                tokens=self.tokens.copy()
            )

# def transform_rolled_dice_pool_prob_dist_to_rolled_dice_pool_prob_dist(
#         probability_distribution: pd.ProbabilityDistribution,
#         rolled_dice_pool_cls: type(RolledDicePool) = RolledDicePool,
# ):
#     prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
#     for stochastic_state, prob in probability_distribution.as_dict.items():
#         if isinstance(stochastic_state, dse.RolledDouse):
#             prob_dist_after[
#                 rolled_dice_pool_cls.from_rolled_dice_list([stochastic_state])
#             ] += prob
#         else:
#             prob_dist_after[stochastic_state] += prob
#
#     return pd.ProbabilityDistribution(prob_dist_after)

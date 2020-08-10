from typing import Union
import logging

from legion_dice_probs.events import roll as rll
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import dice_pool_with_tokens as dce_wtoks
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import tokens_specialized as toks_spec
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object


class AimReroll(rll.Roll):
    def on(
            self,
            object_: Union[
                dse.RolledDouse,
                dce.RolledDicePool,
                st_object.StochasticObject,
                pd.ProbabilityDistribution,
            ]
    ) -> Union[
        pd.ProbabilityDistribution,
    ]:
        if isinstance(object_, dce_wtoks.RolledDicePoolWithTokens):
            if isinstance(object_.tokens, toks_spec.TokensAttack) or len(object_.tokens) == 0:
                rolled_dice_sorted = sorted(
                    object_.rolled_dice_counter.elements(),
                    key=self.roll_policy.get_douse_roll_priority,
                )
                prob_dists_after = []
                for rolled_douse in rolled_dice_sorted:
                    rerolled_prob_dist = self.on(rolled_douse) if self.can_roll else \
                        rolled_douse.get_probability_distribution()
                    prob_dists_after.append(rerolled_prob_dist)

                # TODO: rethink if this logic should be implemented either as part of DicePool.from_dice_list or
                #  RolledDicePool.aggregate_rolled_dice. Former would extend signature with RolledDouse and latter with
                #  Douse
                aggregated_dice_probability_distribution = object_.aggregate_dice_probability_distributions(
                    prob_dists_after
                )
                return aggregated_dice_probability_distribution

            #     if object_.tokens.count_tokens(toks_spec.AimToken()) > 0:
            #         probability_distribution_after = super().on(object_)
            #         if self.n_rolled:
            #             object_.tokens.remove_token(toks_spec.AimToken())
            #         rolled_dice_pool_after, _ = probability_distribution_after.as_dict.popitem()
            #         rolled_dice_pool_with_tokens_after = dce_wtoks.RolledDicePoolWithTokens(
            #             rolled_dice_counter=rolled_dice_pool_after.rolled_dice_counter,
            #             tokens=object_.tokens,
            #         )
            #         return rolled_dice_pool_with_tokens_after.get_probability_distribution()
            #     else:
            #         return object_.get_probability_distribution()
            else:
                logging.warning(f'Wrong type of tokens: {object_.tokens}.')

        return super().on(object_)

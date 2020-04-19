import logging
from typing import Optional
from typing import Union

from legion_dice_probs.events.tools import conversion_policy as conv_pol
from legion_dice_probs.events import convert_symbols as conv_syms
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import dice_pool_attack as dce_att
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class ConvertSurgeWithTokens(conv_syms.ConvertSymbols):
    # def mark_conversion(
    #         self,
    #         rolled_dice_pool_attack: Optional[dce_att.RolledDicePoolAttack] = None,
    # ):
    #     if not rolled_dice_pool_attack.n_surge_tokens > 0:
    #         logging.warning(f'Not tokens left in {rolled_dice_pool_attack}, but conversion is still marked.')
    #     rolled_dice_pool_attack.n_surge_tokens -= 1
    #
    #     super().mark_conversion()

    # def __init__(self, conversion_policy: conv_pol.ConversionPolicy):
    #     super().__init__(
    #         conversion_policy,
    #         conversion_limit=None,
    #     )

    def on(
            self,
            object_: Union[
                st_state.StochasticState,
                st_object.StochasticObject,
                pd.ProbabilityDistribution,
            ],
    ) -> Union[
        sym.Symbol,
        syms.Symbols,
        dse.RolledDouse,
        dce.RolledDicePool,
        pd.ProbabilityDistribution
    ]:
        if isinstance(object_, dce_att.RolledDicePoolAttack):
            self._conversion_limit = object_.n_surge_tokens
            converted_rolled_dice_pool = super().on(object_)
            return dce_att.RolledDicePoolAttack(
                rolled_dice_counter=converted_rolled_dice_pool.rolled_dice_counter,
                n_surge_tokens=object_.n_surge_tokens - self.n_converted,
                n_aim_tokens=object_.n_aim_tokens,
            )

        if isinstance(object_, dce.RolledDicePool):
            return object_.get_probability_distribution()

        # TODO: remove DicePoolAttack
        if isinstance(object_, dce_att.DicePoolAttack):
            raise NotImplementedError

        if isinstance(object_, dce.DicePool):
            return object_.get_probability_distribution()

        return super().on(object_)

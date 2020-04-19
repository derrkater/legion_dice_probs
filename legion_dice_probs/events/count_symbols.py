from typing import Union

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import dice_pool_attack as dce_att
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms
from legion_dice_probs.stochastic_states import symbols_attack as syms_att
from prob_dist_api import event
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class CountSymbols(event.Event):
    def copy(self) -> "CountSymbols":
        return self.__class__()

    def on(
            self,
            object_: Union[
                st_state.StochasticState,
                st_object.StochasticObject,
                pd.ProbabilityDistribution,
            ]
    ) -> Union[
        syms.Symbols,
        pd.ProbabilityDistribution,
    ]:
        if isinstance(object_, sym.Symbol):
            return syms.Symbols.from_symbols_list([object_])
        if isinstance(object_, syms.Symbols):
            return object_
        if isinstance(object_, dse.RolledDouse):
            return syms.Symbols.from_symbols_list([object_.symbol])

        if isinstance(object_, dce.RolledDicePool):
            symbols_list = [rolled_douse.symbol for rolled_douse in object_.rolled_dice_counter.elements()]

            if isinstance(object_, dce_att.RolledDicePoolAttack):
                return syms_att.SymbolsAttack.from_symbols_list(
                    symbols_list=symbols_list,
                    n_surge_tokens=object_.n_surge_tokens,
                    n_aim_tokens=object_.n_aim_tokens,
                )
            else:
                return syms.Symbols.from_symbols_list(
                    symbols_list=symbols_list,
                )

        return super().on(object_)

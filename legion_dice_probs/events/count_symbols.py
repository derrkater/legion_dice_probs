import collections
import fractions
from typing import Union

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms

from prob_dist_api import event
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class CountSymbols(event.Event):
    @classmethod
    def on(
            cls,
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
            return syms.Symbols.from_symbols_list(
                symbols_list=[rolled_douse.symbol for rolled_douse in object_.rolled_dice_counter.elements()],
            )
        if isinstance(object_, st_object.StochasticObject):
            prob_dist = object_.get_probability_distribution()
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in prob_dist.as_dict.items():
                prob_dist_after[cls.on(state)] += prob

            return pd.ProbabilityDistribution(prob_dist_after)

        if isinstance(object_, pd.ProbabilityDistribution):
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in object_.as_dict.items():
                prob_dist_after[cls.on(state)] += prob

            return pd.ProbabilityDistribution(prob_dist_after)

        raise NotImplementedError(f'{type(object_)} is not supported.')

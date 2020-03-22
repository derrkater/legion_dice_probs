"""
Conversion policies.

Attack policies
All convert to crit. First blank, surge, hit. First white, black red.
All but crit convert to hit. First blank, surge. First white, black, red.

Block policy
hit to blank // cover
crit to blank - special rule of clones tank

Calculate results
surge to blank
"""

import collections
import fractions
import logging
from typing import Union

from legion_dice_probs.events.tools import conversion_policy as conv_pol
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms
from prob_dist_api import event
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class ConvertSymbols(event.Event):
    def __init__(
            self,
            conversion_policy: conv_pol.ConversionPolicy,
            conversion_limit: int = None,
    ):
        if conversion_limit is not None and conversion_limit < 1:
            raise ValueError(f'Requested {conversion_limit} conversions.')

        self.conversion_policy = conversion_policy
        self._conversion_limit = conversion_limit
        self._n_converted = 0

    @property
    def conversion_target(self) -> sym.Symbol:
        return self.conversion_policy.conversion_target

    @property
    def conversion_limit(self):
        return self._conversion_limit

    @property
    def n_converted(self):
        return self._n_converted

    @property
    def can_convert(self):
        return self.conversion_limit is None or self.n_converted < self.conversion_limit

    def mark_conversion(self):
        if not self.can_convert:
            logging.warning(f'Marking conversion with {self}, while conversion limit of {self.conversion_limit}')
        self._n_converted += 1

    def copy(self) -> "ConvertSymbols":
        return self.__class__(
            conversion_policy=self.conversion_policy,
            conversion_limit=self.conversion_limit,
        )

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
        if isinstance(object_, sym.Symbol):
            if self.conversion_policy.is_convertible(object_):
                self.mark_conversion()
                return self.conversion_target
            else:
                return object_
        if isinstance(object_, syms.Symbols):
            symbols_sorted = sorted(
                object_.symbols_counter.elements(),
                key=self.conversion_policy.get_symbol_conversion_priority,
            )
            symbols_converted = []
            for symbol in symbols_sorted:
                symbol_converted = self.on(symbol) if self.can_convert else symbol
                symbols_converted.append(symbol_converted)

            return syms.Symbols.from_symbols_list(symbols_converted)

        if isinstance(object_, dse.RolledDouse):
            symbol_after = self.on(object_.symbol)
            if symbol_after not in object_.douse.get_sides():
                raise ValueError(f'Conversion {self} cannot be applied to {object_}, because it does not have target '
                                 f'side')
            if self.conversion_target not in object_.douse.get_sides():
                logging.warning(f'Conversion of wrong type {self} applied to {object_}.')
            return dse.RolledDouse(
                douse=object_.douse,
                symbol=symbol_after,
            )
        if isinstance(object_, dce.RolledDicePool):
            rolled_dice_sorted = sorted(
                object_.rolled_dice_counter.elements(),
                key=self.conversion_policy.get_douse_conversion_priority,
            )
            rolled_dice_converted = []
            for rolled_douse in rolled_dice_sorted:
                symbol_converted = self.on(rolled_douse) if self.can_convert else rolled_douse
                rolled_dice_converted.append(symbol_converted)

            return dce.RolledDicePool.from_rolled_dice_list(rolled_dice_converted)

        if isinstance(object_, st_object.StochasticObject):
            prob_dist = object_.get_probability_distribution()
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in prob_dist.as_dict.items():
                prob_dist_after[self.copy().on(state)] += prob

            return pd.ProbabilityDistribution(prob_dist_after)

        if isinstance(object_, pd.ProbabilityDistribution):
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in object_.as_dict.items():
                prob_dist_after[self.copy().on(state)] += prob

            return pd.ProbabilityDistribution(prob_dist_after)

        raise NotImplementedError(f'{type(object_)} is not supported.')

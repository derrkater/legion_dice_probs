import collections
import fractions
import logging
from abc import abstractmethod, ABC
from typing import Union

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms

from prob_dist_api import event
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


# todo Symbols and RolledDicePool cases are very similar as they both are wrappers on counter objects. Refactor?
class ConvertSurge(event.Event, ABC):
    @classmethod
    @abstractmethod
    def surge_conversion_target(cls) -> sym.Symbol:
        raise NotImplementedError

    @classmethod
    def on(
            cls,
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
            return cls.surge_conversion_target() if isinstance(object_, sym.Surge) else object_
        if isinstance(object_, syms.Symbols):
            symbols_counter = object_.symbols_counter
            symbols_counter_dict_after = collections.defaultdict(lambda: 0)
            for symbol, count in symbols_counter.items():
                symbols_counter_dict_after[cls.on(symbol)] += count
            return syms.Symbols(
                symbols_counter=collections.Counter(symbols_counter_dict_after)
            )
        if isinstance(object_, dse.RolledDouse):
            symbol_after = cls.on(object_.symbol)
            if symbol_after not in object_.douse.get_sides():
                raise ValueError(f'Conversion {cls} cannot be applied to {object_}, because it does not have target '
                                 f'side')
            if cls.surge_conversion_target() not in object_.douse.get_sides():
                logging.warning(f'Conversion of wrong type {cls} applied to {object_}.')
            return dse.RolledDouse(
                douse=object_.douse,
                symbol=symbol_after,
            )
        if isinstance(object_, dce.RolledDicePool):
            rolled_dice_counter = object_.rolled_dice_counter
            rolled_dice_dict_after = collections.defaultdict(lambda: 0)
            for rolled_douse, count in rolled_dice_counter.items():
                rolled_dice_dict_after[cls.on(rolled_douse)] += count
            return dce.RolledDicePool(
                rolled_dice_counter=collections.Counter(rolled_dice_dict_after)
            )
        if isinstance(object_, st_object.StochasticObject):
            prob_dist = object_.get_probability_distribution()
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in prob_dist.as_dict.items():
                prob_dist_after[cls.on(state)] += prob

            return pd.ProbabilityDistribution(prob_dist_after)

        raise NotImplementedError(f'{type(object_)} is not supported.')


class ConvertSurgeHit(ConvertSurge):

    @classmethod
    def surge_conversion_target(cls) -> sym.Hit:
        return sym.Hit()


class ConvertSurgeCrit(ConvertSurge):

    @classmethod
    def surge_conversion_target(cls) -> sym.Crit:
        return sym.Crit()


class ConvertSurgeBlock(ConvertSurge):

    @classmethod
    def surge_conversion_target(cls) -> sym.Block:
        return sym.Block()

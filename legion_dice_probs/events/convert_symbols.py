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
from abc import ABC
from typing import Tuple
from typing import Union

from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym
from legion_dice_probs.stochastic_states import symbols as syms

from prob_dist_api import event
from prob_dist_api import probability_distribution as pd
from prob_dist_api import stochastic_object as st_object
from prob_dist_api import stochastic_state as st_state


class ConversionPolicy(ABC):
    def __init__(
            self,
            conversion_target: sym.Symbol,
    ):
        self.conversion_target = conversion_target

    @classmethod
    def get_convertible_symbols(cls):
        raise NotImplementedError

    @classmethod
    def get_convertible_dice(cls):
        raise NotImplementedError

    def is_convertible(
            self,
            symbol: sym.Symbol,
    ):
        return any(
            isinstance(
                symbol,
                convertible_symbol_cls,
            ) for convertible_symbol_cls in self.get_convertible_symbols()
        )

    def index(
            self,
            symbol: sym.Symbol,
    ):
        return self.get_convertible_symbols().index(type(symbol))


class ConversionPolicyAttack(ConversionPolicy, ABC):
    @classmethod
    def get_convertible_dice(cls):
        return (
            att_dse.WhiteAttackDouse,
            att_dse.BlackAttackDouse,
            att_dse.RedAttackDouse,
        )


class ConversionPolicyAttackAnyToCrit(ConversionPolicyAttack):
    def __init__(
            self,
            conversion_target: sym.Symbol = sym.Crit(),
    ):
        super().__init__(conversion_target)

    @classmethod
    def get_convertible_symbols(cls):
        return (
            sym.Blank,
            sym.Surge,
            sym.Hit,
        )


class ConversionPolicyAttackAnyToHit(ConversionPolicyAttack):
    def __init__(
            self,
            conversion_target: sym.Symbol = sym.Hit(),
    ):
        super().__init__(conversion_target)

    @classmethod
    def get_convertible_symbols(cls):
        return (
            sym.Blank,
            sym.Surge,
        )


class ConversionPolicyAttackSurgeToHit(ConversionPolicyAttack):
    def __init__(
            self,
            conversion_target: sym.Symbol = sym.Hit(),
    ):
        super().__init__(conversion_target)

    @classmethod
    def get_convertible_symbols(cls):
        return sym.Surge,


class ConversionPolicyAttackSurgeToCrit(ConversionPolicyAttack):
    def __init__(
            self,
            conversion_target: sym.Symbol = sym.Crit(),
    ):
        super().__init__(conversion_target)

    @classmethod
    def get_convertible_symbols(cls):
        return sym.Surge,


class ConversionPolicyDefend(ConversionPolicy, ABC):
    @classmethod
    def get_convertible_dice(cls):
        return NotImplemented,


class ConversionPolicyAttackSurgeToBlock(ConversionPolicyDefend):
    def __init__(
            self,
            conversion_target: sym.Symbol = sym.Block(),
    ):
        super().__init__(conversion_target)

    @classmethod
    def get_convertible_symbols(cls):
        return sym.Surge,


class ConvertSymbols(event.Event):
    def __init__(
            self,
            conversion_policy: ConversionPolicy,
            n_converts: int = None,
    ):
        if n_converts is not None and n_converts < 1:
            raise ValueError(f'Requested {n_converts} conversions.')

        self.conversion_policy = conversion_policy
        self.n_converts = n_converts

    @property
    def conversion_target(self) -> sym.Symbol:
        return self.conversion_policy.conversion_target

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
            return self.conversion_target if self.conversion_policy.is_convertible(object_) else object_
        if isinstance(object_, syms.Symbols):
            symbols = object_.symbols_counter.elements()

            def get_symbol_conversion_priority(symbol: sym.Symbol):
                if not self.conversion_policy.is_convertible(symbol):
                    return len(self.conversion_policy.get_convertible_symbols())
                else:
                    return self.conversion_policy.index(symbol)

            symbols_sorted = sorted(
                symbols,
                key=get_symbol_conversion_priority,
            )
            n_converted = 0
            symbols_converted = []
            for symbol in symbols_sorted:
                if self.n_converts is None or n_converted < self.n_converts:
                    symbol_converted = self.on(symbol)

                    if symbol_converted != symbol:
                        n_converted += 1
                else:
                    symbol_converted = symbol

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
            rolled_dice_counter = object_.rolled_dice_counter
            rolled_dice_dict_after = collections.defaultdict(lambda: 0)
            for rolled_douse, count in rolled_dice_counter.items():
                rolled_dice_dict_after[self.on(rolled_douse)] += count
            return dce.RolledDicePool(
                rolled_dice_counter=collections.Counter(rolled_dice_dict_after)
            )
        if isinstance(object_, st_object.StochasticObject):
            prob_dist = object_.get_probability_distribution()
            prob_dist_after = collections.defaultdict(lambda: fractions.Fraction(0))
            for state, prob in prob_dist.as_dict.items():
                prob_dist_after[self.on(state)] += prob

            return pd.ProbabilityDistribution(prob_dist_after)

        raise NotImplementedError(f'{type(object_)} is not supported.')

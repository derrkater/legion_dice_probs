from abc import ABC
from typing import Union

from legion_dice_probs.stochastic_objects import douse as dse, attack_douse as att_dse
from legion_dice_probs.stochastic_states import symbol as sym


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
            object_: Union[sym.Symbol, dse.RolledDouse],
    ):
        if isinstance(object_, sym.Symbol):
            return any(
                isinstance(
                    object_,
                    convertible_symbol_cls,
                ) for convertible_symbol_cls in self.get_convertible_symbols()
            )
        if isinstance(object_, dse.RolledDouse):
            return any(
                (
                        isinstance(object_, convertible_douse_cls) and
                        self.is_convertible(object_.symbol)
                ) for convertible_douse_cls in self.get_convertible_dice()
            )

    def index(
            self,
            symbol: sym.Symbol,
    ):
        return self.get_convertible_symbols().index(type(symbol))

    def rolled_douse_index(
            self,
            douse: dse.RolledDouse,
    ):
        return self.get_convertible_dice().index(type(douse))

    def get_symbol_conversion_priority(
            self,
            symbol: sym.Symbol,
    ):
        if not self.is_convertible(symbol):
            return len(self.get_convertible_symbols())
        else:
            return self.index(symbol)

    def get_douse_conversion_priority(
            self,
            douse: dse.RolledDouse,
    ):
        if not self.is_convertible(douse):
            return len(self.get_convertible_symbols()), len(self.get_convertible_dice())
        else:
            return self.index(douse.symbol), self.rolled_douse_index(douse)


class ConversionPolicyAttack(ConversionPolicy, ABC):
    @classmethod
    def get_convertible_dice(cls):
        return (
            att_dse.RolledWhiteAttackDouse,
            att_dse.RolledBlackAttackDouse,
            att_dse.RolledRedAttackDouse,
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
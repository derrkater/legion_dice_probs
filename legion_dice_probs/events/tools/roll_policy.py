from abc import ABC
from typing import Tuple
from typing import Type
from typing import Union

from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import defence_douse as def_dse
from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym


class RollPolicy(ABC):
    def __init__(
            self,
            dice_number: int = None,
    ):
        self.dice_number = dice_number

    @classmethod
    def get_rollable_symbols(cls) -> Tuple[Type[sym.Symbol]]:
        raise NotImplementedError

    @classmethod
    def get_rollable_dice(cls) -> Tuple[Type[dse.Douse]]:
        raise NotImplementedError

    def is_rollable(
            self,
            object_: Union[
                sym.Symbol,
                dse.RolledDouse,
                dse.Douse,
            ],
    ):
        if isinstance(object_, sym.Symbol):
            return any(
                isinstance(
                    object_,
                    rerollable_symbol_cls,
                ) for rerollable_symbol_cls in self.get_rollable_symbols()
            )
        if isinstance(object_, dse.RolledDouse):
            return any(
                (
                        self.is_rollable(object_.symbol) and
                        isinstance(object_.douse, rerollable_douse_cls)

                ) for rerollable_douse_cls in self.get_rollable_dice()
            )
        if isinstance(object_, dse.Douse):
            return any(
                isinstance(
                    object_,
                    rollable_douse_cls,
                ) for rollable_douse_cls in self.get_rollable_dice()
            )
        raise ValueError


class RollPolicyAttack(RollPolicy):
    @classmethod
    def get_rollable_dice(cls):
        return (
            att_dse.RedAttackDouse,
            att_dse.BlackAttackDouse,
            att_dse.WhiteAttackDouse,
        )

    @classmethod
    def get_rollable_symbols(cls):
        return (
            sym.Blank,
            sym.Surge,
        )


class RollPolicyAttackBlanksOnly(RollPolicyAttack):
    @classmethod
    def get_rollable_symbols(cls):
        return (
            sym.Blank,
        )


class RollPolicyAttackCritFish(RollPolicyAttack):
    @classmethod
    def get_rollable_symbols(cls):
        return (
            sym.Blank,
            sym.Surge,
            sym.Hit,
        )


class RollPolicyDefence(RollPolicy):
    @classmethod
    def get_rollable_dice(cls):
        return (
            def_dse.RedDefenceDouse,
            def_dse.WhiteDefenceDouse,
        )

    @classmethod
    def get_rollable_symbols(cls):
        return (
            sym.Blank,
            sym.Surge,
        )

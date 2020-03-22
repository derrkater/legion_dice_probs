from abc import ABC

from legion_dice_probs.stochastic_objects import attack_douse as att_dse
from legion_dice_probs.stochastic_objects import defence_douse as def_dse
from legion_dice_probs.stochastic_states import symbol as sym


class RollPolicy(ABC):
    def __init__(
            self,
            dice_number: int = None,
    ):
        pass

    @classmethod
    def get_rollable_symbols(cls):
        raise NotImplementedError

    @classmethod
    def get_rollable_dice(cls):
        raise NotImplementedError


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


from legion_dice_probs.events import convert_symbols as conv_syms
from legion_dice_probs.events.tools import conversion_policy as conv_pol


class ConvertSurgesToHit(conv_syms.ConvertSymbols):
    def __init__(
            self,
            conversion_policy: conv_pol.ConversionPolicy = None,
            conversion_limit: int = None,
    ):
        super().__init__(
            conversion_policy=conversion_policy or conv_pol.ConversionPolicyAttackSurgeToHit(),
            conversion_limit=conversion_limit,
        )


class ConvertSurgesToCrit(conv_syms.ConvertSymbols):
    def __init__(
            self,
            conversion_policy: conv_pol.ConversionPolicy = None,
            conversion_limit: int = None,
    ):
        super().__init__(
            conversion_policy=conversion_policy or conv_pol.ConversionPolicyAttackSurgeToCrit(),
            conversion_limit=conversion_limit,
        )


class ConvertSurgesToBlock(conv_syms.ConvertSymbols):
    def __init__(
            self,
            conversion_policy: conv_pol.ConversionPolicy = None,
            conversion_limit: int = None,
    ):
        super().__init__(
            conversion_policy=conversion_policy or conv_pol.ConversionPolicyAttackSurgeToBlock(),
            conversion_limit=conversion_limit,
        )

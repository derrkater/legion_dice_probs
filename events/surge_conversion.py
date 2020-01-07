from typing import Union

import dice_symbols as sym
from events import event
import roll_result


class SurgeConversion(event.EventDeterministic):
    @classmethod
    def get_target_symbol(cls):
        raise NotImplementedError

    @classmethod
    def deterministic_event_on_key(cls, prob_dist_key: Union[sym.Symbol, roll_result.RollResult]):
        if not isinstance(prob_dist_key, sym.Symbol) and not issubclass(type(prob_dist_key), roll_result.RollResult):
            raise ValueError(f'Event {cls} cannot be applied to {prob_dist_key}.')

        if issubclass(type(prob_dist_key), roll_result.RollResult):
            return cls.apply(prob_dist_key, target_cls=roll_result.RollResult.from_counter)
        elif isinstance(prob_dist_key, sym.Surge):
            return cls.get_target_symbol()
        else:
            return prob_dist_key


class NoSurgeConversion(SurgeConversion):
    @classmethod
    def get_target_symbol(cls):
        return sym.Blank()


class SurgeToHitConversion(SurgeConversion):
    @classmethod
    def get_target_symbol(cls):
        return sym.Hit()


class SurgeToCritConversion(SurgeConversion):
    @classmethod
    def get_target_symbol(cls):
        return sym.Crit()


class SurgeToDodgeConversion(SurgeConversion):
    @classmethod
    def get_target_symbol(cls):
        return sym.Block()

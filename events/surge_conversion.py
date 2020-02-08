from typing import Union

import dice
import dice_colors as col
from events import event


class SurgeConversion(event.EventDeterministic):
    @classmethod
    def get_target_symbol(cls, color: type(col.Color)):
        raise NotImplementedError

    @classmethod
    def deterministic_event_on_key(cls, prob_dist_key: Union[dice.Symbol, dice.RollResult]):
        if not isinstance(prob_dist_key, dice.Symbol) and not issubclass(type(prob_dist_key), dice.RollResult):
            raise ValueError(f'Event {cls} cannot be applied to {prob_dist_key}.')

        if issubclass(type(prob_dist_key), dice.RollResult):
            return cls.apply(
                prob_dist_key,
                target_cls=dice.RollResult.from_counter
            )
        elif isinstance(prob_dist_key, dice.Surge):
            return cls.get_target_symbol(prob_dist_key.douse)
        else:
            return prob_dist_key


class NoSurgeConversion(SurgeConversion):
    @classmethod
    def get_target_symbol(cls, color: type(col.Color)):
        return dice.Blank(color)


class SurgeToHitConversion(SurgeConversion):
    @classmethod
    def get_target_symbol(cls, color: type(col.Color)):
        return dice.Hit(color)


class SurgeToCritConversion(SurgeConversion):
    @classmethod
    def get_target_symbol(cls, color: type(col.Color)):
        return dice.Crit(color)


class SurgeToDodgeConversion(SurgeConversion):
    @classmethod
    def get_target_symbol(cls, color: type(col.Color)):
        return dice.Block(color)

from typing import Union

import dice_symbols as sym
import event
import roll_results


class SurgeConversion(event.EventOnKeys):
    @classmethod
    def get_target_symbol(cls):
        raise NotImplementedError

    @classmethod
    def event_on_keys(cls, prob_dist_key: Union[sym.Symbol, roll_results.RollResult]):
        if not isinstance(prob_dist_key, sym.Symbol) and not issubclass(type(prob_dist_key), roll_results.RollResult):
            raise ValueError(f'Event {cls} cannot be applied to {prob_dist_key}.')

        if issubclass(type(prob_dist_key), roll_results.RollResult):
            transformed_roll_result = cls.apply(prob_dist_key, target_cls=roll_results.RollResult.from_counter)
            print(transformed_roll_result)
            return transformed_roll_result
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

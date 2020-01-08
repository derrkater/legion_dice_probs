from typing import Union

from events import event
import dice_symbols as sym
import roll_result as rr


class RemoveColorsEvent(event.EventDeterministic):
    @classmethod
    def deterministic_event_on_key(cls, prob_dist_key: Union[sym.Symbol, rr.RollResult]):
        if not isinstance(prob_dist_key, sym.Symbol) and not issubclass(type(prob_dist_key), rr.RollResult):
            raise ValueError(f'Event {cls} cannot be applied to {prob_dist_key}.')

        if issubclass(type(prob_dist_key), rr.RollResult):
            return cls.apply(
                prob_dist_key,
                target_cls=rr.RollResult.from_counter
            )
        elif issubclass(type(prob_dist_key), sym.Symbol):
            return prob_dist_key.__class__(color=None)
        else:
            raise NotImplementedError

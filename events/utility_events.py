from typing import Union

from events import event
import dice


class RemoveColorsEvent(event.EventDeterministic):
    @classmethod
    def deterministic_event_on_key(cls, prob_dist_key: Union[dice.Symbol, dice.RollResult]):
        if not isinstance(prob_dist_key, dice.Symbol) and not issubclass(type(prob_dist_key), dice.RollResult):
            raise ValueError(f'Event {cls} cannot be applied to {prob_dist_key}.')

        if issubclass(type(prob_dist_key), dice.RollResult):
            return cls.apply(
                prob_dist_key,
                target_cls=dice.RollResult.from_counter
            )
        elif isinstance(prob_dist_key, dice.Symbol):
            return prob_dist_key.__class__(douse=None)
        else:
            raise NotImplementedError()

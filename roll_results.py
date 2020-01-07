from collections import Counter
from typing import List, Union

import dice
import dice_symbols as sym


class ResultNegativeError(ValueError):
    pass


class DiceResultEmptyError(ValueError):
    pass


class RollResult(Counter):
    def __init__(self, results_list: List[Union[sym.Symbol, "RollResult"]]):
        if any(
                (
                        not issubclass(type(r), sym.Symbol) and
                        not issubclass(type(r), RollResult)
                ) for r in results_list
        ):
            raise ValueError(f'All inputs should be {sym.Symbol} or {RollResult}. [{results_list}]')

        self._results_list = [[r] if issubclass(type(r), sym.Symbol) else r._results_list for r in results_list]
        self._results_list = [symbol for r in self._results_list for symbol in r]
        super().__init__(self._results_list)

    def __hash__(self):
        return hash(frozenset(self.items()))

    def __add__(self, other):
        if issubclass(other.__class__, RollResult):
            return RollResult(self._results_list + other._results_list)
        elif issubclass(other.__class__, dice.Douse):
            return RollResult(self._results_list + other.events_list)
        else:
            raise ValueError(f'Does not support type {other.__class__}.')

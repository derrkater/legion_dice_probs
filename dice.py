import collections
from abc import ABC
from typing import List, Union

import dice_colors as col
import dice_pool
import prob_dist as pd


class Symbol(pd.StochasticState):
    def __init__(self):
        super().__init__()

    def in_prob_dist(self, prob_dist: "Douse"):
        super().in_prob_dist(prob_dist)

    @property
    def color(self):
        return self.prob_dist.color

    def __repr__(self):
        # return str(self.__class__.__name__)
        if self.color is None:
            return self.__class__.__name__
        return f'{self.__class__.__name__}_{self.color}'

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __hash__(self):
        return hash(self.__repr__())


class Crit(Symbol):
    pass


class Hit(Symbol):
    pass


class Surge(Symbol):
    pass


class Block(Symbol):
    pass


class Blank(Symbol):
    pass


class Douse(pd.ProbDist, ABC):

    def __init__(self, **kwargs):
        super().__init__(
            collections.Counter(self.events_list),
            **kwargs
        )

    @property
    def color(self):
        raise NotImplementedError

    @property
    def _symbols_list(self) -> List[type(Symbol)]:
        raise NotImplementedError

    @property
    def events_list(self) -> List[Symbol]:
        return [symbol_cls() for symbol_cls in self._symbols_list]

    @property
    def aggregation_class(self):
        return dice_pool.DicePool

    @property
    def keys_merge_function(self):
        return lambda x, y: RollResult([x, y])

    def __add__(self, other):
        if issubclass(type(other), Douse) or issubclass(type(other), dice_pool.DicePool):
            return super().__add__(other)
        else:
            super().__add__(other)


class AttackDouse(Douse, ABC):
    pass


class RedAttackDouse(AttackDouse):
    @property
    def color(self):
        return col.Red()

    @property
    def _symbols_list(self) -> List[type(Symbol)]:
        return [
            Crit,
            Surge,
            Hit,
            Hit,
            Hit,
            Hit,
            Hit,
            Blank,
        ]


class BlackAttackDouse(AttackDouse):
    @property
    def color(self):
        return col.Black()

    @property
    def _symbols_list(self) -> List[type(Symbol)]:
        return [
            Crit,
            Surge,
            Hit,
            Hit,
            Hit,
            Blank,
            Blank,
            Blank,
        ]


class WhiteAttackDouse(AttackDouse):
    @property
    def color(self):
        return col.White()

    @property
    def _symbols_list(self) -> List[type(Symbol)]:
        return [
            Crit,
            Surge,
            Hit,
            Blank,
            Blank,
            Blank,
            Blank,
            Blank,
        ]


class DefenceDouse(Douse, ABC):
    pass


class RedDefenceDouse(DefenceDouse):
    @property
    def color(self):
        return col.Red()

    @property
    def _symbols_list(self) -> List[type(Symbol)]:
        return [
            Surge,
            Block,
            Block,
            Block,
            Blank,
            Blank,
        ]


class WhiteDefenceDouse(DefenceDouse):
    @property
    def color(self):
        return col.White()

    @property
    def _symbols_list(self) -> List[type(Symbol)]:
        return [
            Surge,
            Block,
            Blank,
            Blank,
            Blank,
            Blank,
        ]


class RollResult(collections.Counter):
    def __init__(self, results_list: List[Union[Symbol, "RollResult"]]):
        if any(
                (
                        not issubclass(type(r), Symbol) and
                        not issubclass(type(r), RollResult)
                ) for r in results_list
        ):
            raise ValueError(f'All inputs should be {Symbol} or {RollResult}. [{results_list}]')

        self._results_list = [[r] if issubclass(type(r), Symbol) else r._results_list for r in results_list]
        self._results_list = [symbol for r in self._results_list for symbol in r]
        super().__init__(self._results_list)

    @classmethod
    def from_counter(cls, counter) -> "RollResult":
        results_list = []
        for key, val in counter.items():
            results_list.extend([key] * val)
        return cls(results_list)

    def __hash__(self):
        return hash(frozenset(self.items()))

    def __add__(self, other):
        if issubclass(other.__class__, RollResult):
            return RollResult(self._results_list + other._results_list)
        elif issubclass(other.__class__, Douse):
            return RollResult(self._results_list + other.events_list)
        else:
            raise ValueError(f'Does not support type {other.__class__}.')

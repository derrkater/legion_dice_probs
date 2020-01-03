from abc import ABC
from dataclasses import dataclass


class ResultNegativeError(ValueError):
    pass


class DiceResultEmptyError(ValueError):
    pass


@dataclass
class RollResult(ABC):
    n_surge: int = 0
    n_blank: int = 0

    def __post_init__(self):
        if self.n_surge < 0 or self.n_blank < 0:
            raise ResultNegativeError

    @property
    def n_results(self):
        return self.n_surge + self.n_blank


@dataclass
class AttackRollResult(RollResult):
    n_crit: int = 0
    n_hit: int = 0

    def __post_init__(self):
        super().__post_init__()

        if self.n_hit < 0 or self.n_crit < 0:
            raise ResultNegativeError

        if not self.n_results:
            raise DiceResultEmptyError

    @property
    def n_results(self):
        return super().n_results + self.n_crit + self.n_hit


@dataclass
class DefenceRollResult(RollResult):
    n_block: int = 0

    def __post_init__(self):
        super().__post_init__()

        if self.n_block < 0:
            raise ResultNegativeError

        if not self.n_results:
            raise DiceResultEmptyError

    @property
    def n_results(self):
        return super().n_results + self.n_block

from abc import ABC
from dataclasses import dataclass


@dataclass
class RollResult(ABC):
    n_surge: int = 0
    n_blank: int = 0

    def __post_init__(self):
        if self.n_surge < 0 or self.n_blank < 0:
            raise ValueError('Attack results no. cannot be negative.')

    @property
    def n_results(self):
        return self.n_surge + self.n_blank


@dataclass
class AttackResult(RollResult):
    n_crit: int = 0
    n_hit: int = 0

    def __post_init__(self):
        super().__post_init__()

        if self.n_hit < 0 or self.n_crit < 0:
            raise ValueError('Attack results no. cannot be negative.')

        if not self.n_results:
            raise ValueError('Attack result needs to have at least one dice result')

    @property
    def n_results(self):
        return super().n_results + self.n_crit + self.n_hit

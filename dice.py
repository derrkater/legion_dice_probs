from abc import ABC
from dataclasses import dataclass


class Douse(ABC):
    pass


class AttackDouse(Douse, ABC):
    crit_prob = 1. / 8
    surge_prob = 1. / 8


class RedAttackDouse(AttackDouse):
    hit_prob = 5. / 8
    blank_prob = 1. / 8


class BlackAttackDouse(AttackDouse):
    hit_prob = 3. / 8
    blank_prob = 3. / 8


class WhiteAttackDouse(AttackDouse):
    hit_prob = 1. / 8
    blank_prob = 5. / 8


class DefenceDouse(Douse, ABC):
    surge_prob = 1. / 6


class RedDefenceDouse(DefenceDouse):
    block_prob = 3. / 6
    blank_prob = 2. / 6


class WhiteDefenceDouse(DefenceDouse):
    block_prob = 1. / 6
    blank_prob = 4. / 6


class DiceNumberNegativeError(ValueError):
    pass


class DicePoolEmptyError(ValueError):
    pass


class DicePool(ABC):
    pass


@dataclass
class AttackDicePool(DicePool):
    n_red: int = 0
    n_black: int = 0
    n_white: int = 0

    def __post_init__(self):
        if self.n_red < 0 or self.n_black < 0 or self.n_white < 0:
            raise DiceNumberNegativeError

        if not self.n_dice:
            raise DicePoolEmptyError

    @property
    def n_dice(self):
        return self.n_red + self.n_black + self.n_white


@dataclass
class DefenceDicePool(DicePool):
    n_red: int = 0
    n_white: int = 0

    def __post_init__(self):
        if self.n_red < 0 or self.n_white < 0:
            raise DiceNumberNegativeError

        if not self.n_dice:
            raise DicePoolEmptyError

    @property
    def n_dice(self):
        return self.n_red + self.n_white

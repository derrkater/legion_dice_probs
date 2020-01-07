from abc import ABC, abstractmethod

import dice


class SurgeConversion(ABC):
    @abstractmethod
    def apply(self, douse: dice.Douse):
        raise NotImplementedError


class NoSurgeConversion(SurgeConversion):
    def apply(self, douse: dice.Douse):
        pass


class SurgeToHitConversion(SurgeConversion):
    def apply(self, douse: dice.AttackDouse):
        pass


class SurgeToCritConversion(SurgeConversion):
    def apply(self, douse: dice.AttackDouse):
        pass


class SurgeToDodgeConversion(SurgeConversion):
    def apply(self, douse: dice.DefenceDouse):
        pass

from abc import ABC, abstractmethod

from dice import Douse


class SurgeConversion(ABC):
    @abstractmethod
    def apply(self, douse: Douse):
        raise NotImplementedError


class NoSurgeConversion(SurgeConversion):
    def apply(self, douse: Douse):
        pass


class SurgeToHitConversion(SurgeConversion):
    def apply(self, douse: Douse):
        pass


class SurgeToCritConversion(SurgeConversion):
    def apply(self, douse: Douse):
        pass


class SurgeToDodgeConversion(SurgeConversion):
    def apply(self, douse: Douse):
        pass

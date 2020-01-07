import collections
from abc import ABC

import prob_dist as pd


class Event(ABC):
    @classmethod
    def apply(cls, prob_dist: pd.ProbDist) -> pd.ProbDist:
        raise NotImplementedError


class EventOnKeys(Event):

    @classmethod
    def event_on_keys(cls, prob_dist_key):
        raise NotImplementedError

    @classmethod
    def apply(cls, prob_dist: pd.ProbDist, target_cls=pd.ProbDist) -> pd.ProbDist:
        prob_dist_transformed = collections.defaultdict(lambda: 0)
        for key, val in prob_dist.items():
            key_transformed = cls.event_on_keys(key)
            prob_dist_transformed[key_transformed] += val
        return target_cls(prob_dist_transformed)

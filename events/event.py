import collections
from abc import ABC

import prob_dist as pd


class Event(ABC):
    @classmethod
    def apply(cls, prob_dist: pd.ProbDist) -> pd.ProbDist:
        raise NotImplementedError


class EventDeterministic(Event):

    @classmethod
    def deterministic_event_on_key(cls, prob_dist_key: pd.StochasticState) -> pd.StochasticState:
        raise NotImplementedError

    @classmethod
    def apply(cls, prob_dist: pd.ProbDist, target_cls=pd.ProbDist) -> pd.ProbDist:
        prob_dist_transformed = collections.defaultdict(lambda: 0)
        for key, prob in prob_dist.items():
            key_transformed = cls.deterministic_event_on_key(key)
            prob_dist_transformed[key_transformed] += prob
        return target_cls(prob_dist_transformed)


class EventProbabilistic(Event):

    @classmethod
    def probabilistic_event_on_key(cls, prob_dist_key: pd.StochasticState) -> pd.ProbDist:
        raise NotImplementedError

    @classmethod
    def apply(cls, prob_dist: pd.ProbDist, target_cls=pd.ProbDist) -> pd.ProbDist:
        prob_dist_transformed = collections.defaultdict(lambda: 0)
        for key, prob in prob_dist.items():
            key_related_sub_prob_dist = cls.probabilistic_event_on_key(key)
            for sub_key, sub_prob in key_related_sub_prob_dist.items():
                prob_dist_transformed[sub_key] += prob * sub_prob
        return target_cls(prob_dist_transformed)

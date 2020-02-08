import prob_dist as pd
from events import event


class IntState(pd.StochasticState):
    def __init__(self, k: int):
        super().__init__()
        self.k = k

    def __repr__(self):
        return str(self.k)

    def __hash__(self):
        return hash(self.k)

    def __eq__(self, other):
        return self.k == other.k


class ReShuffle(event.EventProbabilistic):

    @classmethod
    def probabilistic_event_on_key(cls, prob_dist_key: IntState) -> pd.ProbDist:
        return prob_dist_key.prob_dist if prob_dist_key.k == 1 else pd.ProbDist.from_events_list([prob_dist_key])


l = [IntState(i) for i in [1, 2, 1, 1, 3]]

p = prob_dist.ProbDist.from_events_list(l)
print(p)
r = ReShuffle.apply(p)
print(r)

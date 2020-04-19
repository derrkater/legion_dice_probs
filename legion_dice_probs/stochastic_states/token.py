from prob_dist_api import stochastic_state as st_state


class Token(st_state.StochasticState):
    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return hash(type(self).__name__)

    def __repr__(self):
        return type(self).__name__

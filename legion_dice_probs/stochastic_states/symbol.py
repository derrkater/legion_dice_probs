from prob_dist_api import stochastic_state as st_state


class Symbol(st_state.StochasticState):
    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return hash(type(self).__name__)


class Blank(Symbol):
    pass


class Surge(Symbol):
    pass


class Hit(Symbol):
    pass


class Block(Symbol):
    pass


class Crit(Symbol):
    pass

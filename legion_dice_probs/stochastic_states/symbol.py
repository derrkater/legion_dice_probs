from prob_dist_api import stochastic_state as st_state


class Symbol(st_state.StochasticState):
    pass


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

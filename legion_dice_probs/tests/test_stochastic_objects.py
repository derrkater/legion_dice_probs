import collections
from typing import List

from legion_dice_probs.stochastic_objects import douse as dse
from legion_dice_probs.stochastic_states import symbol as sym
from prob_dist_api import probability_distribution as pd


class Sym1(sym.Symbol):
    pass


class Sym2(sym.Symbol):
    pass


class Douse1(dse.Douse):

    def get_sides(self) -> List[sym.Symbol]:
        return [
            Sym1(),
            Sym1(),
            Sym2(),
        ]

    @staticmethod
    def get_rolled_douse_cls() -> type(dse.RolledDouse):
        return dse.RolledDouse


class Douse2(dse.Douse):

    def get_sides(self) -> List[sym.Symbol]:
        return [
            Sym1(),
            Sym2(),
            Sym2(),
        ]

    @staticmethod
    def get_rolled_douse_cls() -> type(dse.RolledDouse):
        return dse.RolledDouse


def test_douse__constructor():
    d = Douse1()
    assert True

# def test_douse__should_implement_equal():
#     assert Douse1() == Douse1()
#     assert Douse1() != Douse2()
#
#     alt_prob_dist_1 = pd.ProbabilityDistribution.from_events_list(
#         [
#             Sym1(),
#             Sym2(),
#         ]
#     )
#
#     assert Douse1(alt_prob_dist_1) != Douse1()
#
#
# def test_douse__should_implement_hash():
#     assert len(
#         collections.Counter(
#             [
#                 Douse1(),
#                 Douse1(),
#                 Douse2(),
#             ]
#         )
#     ) == 2
#
#     alt_prob_dist_1 = pd.ProbabilityDistribution.from_events_list(
#         [
#             Sym1(),
#             Sym2(),
#         ]
#     )
#
#     assert len(
#         collections.Counter(
#             [
#                 Douse1(),
#                 Douse1(alt_prob_dist_1),
#                 Douse2(),
#             ]
#         )
#     ) == 3

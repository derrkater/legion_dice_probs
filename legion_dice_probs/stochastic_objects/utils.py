from typing import Union

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import probability_distribution_utils as pd_utils


def aggregate_rolled_douse_into_rolled_dice_pool(
        rolled_douse_1: dse.RolledDouse,
        rolled_douse_2: dse.RolledDouse,
):
    return dce.RolledDicePool.from_rolled_dice_list(
        [
            rolled_douse_1,
            rolled_douse_2,
        ]
    )


DiceObjType = Union[
    dse.Douse,
    dce.DicePool,
]

RolledDiceObjType = Union[
    dse.RolledDouse,
    dce.RolledDicePool,
]


def aggregate_dice(
        dice_obj_1: DiceObjType,
        dice_obj_2: DiceObjType,
) -> dce.DicePool:
    if isinstance(dice_obj_1, dse.Douse) and isinstance(dice_obj_2, dse.Douse):
        return dce.DicePool.from_dice_list(
            [
                dice_obj_1,
                dice_obj_2
            ]
        )
    if isinstance(dice_obj_1, dce.DicePool) and isinstance(dice_obj_2, dce.DicePool):
        return dce.DicePool(
            probability_distribution=pd_utils.aggregate_probability_distributions(
                pd_1=dice_obj_1.get_probability_distribution(),
                pd_2=dice_obj_2.get_probability_distribution(),
                aggregate_function=NotImplemented
            ),
            dice_list=dice_obj_1.dice_list + dice_obj_2.dice_list,
        )
    if isinstance(dice_obj_1, dce.DicePool) and isinstance(dice_obj_2, dse.Douse):
        raise NotImplementedError
    if isinstance(dice_obj_2, dce.DicePool) and isinstance(dice_obj_1, dse.Douse):
        raise NotImplementedError
    raise ValueError


def aggregate_rolled_dice(
        rolled_dice_obj_1: RolledDiceObjType,
        rolled_dice_obj_2: RolledDiceObjType,
) -> dce.RolledDicePool:
    if isinstance(rolled_dice_obj_1, dse.RolledDouse) and isinstance(rolled_dice_obj_2, dse.RolledDouse):
        return dce.RolledDicePool.from_rolled_dice_list(
            [
                rolled_dice_obj_1,
                rolled_dice_obj_2,
            ]
        )
    if isinstance(rolled_dice_obj_1, dce.RolledDicePool) and isinstance(rolled_dice_obj_2, dce.RolledDicePool):
        return dce.RolledDicePool.from_rolled_dice_list(
            list(rolled_dice_obj_1.rolled_dice_counter.elements()) +
            list(rolled_dice_obj_2.rolled_dice_counter.elements())
        )
    if isinstance(rolled_dice_obj_1, dce.RolledDicePool) and isinstance(rolled_dice_obj_2, dse.RolledDouse):
        return dce.RolledDicePool.from_rolled_dice_list(
            list(rolled_dice_obj_1.rolled_dice_counter.elements()) + [rolled_dice_obj_2]
        )
    if isinstance(rolled_dice_obj_2, dce.RolledDicePool) and isinstance(rolled_dice_obj_1, dse.RolledDouse):
        return aggregate_rolled_dice(
            rolled_dice_obj_2,
            rolled_dice_obj_1
        )
    raise ValueError

from typing import Union

from legion_dice_probs.stochastic_objects import dice_pool as dce
from legion_dice_probs.stochastic_objects import douse as dse
from prob_dist_api import probability_distribution_utils as pd_utils

DiceObjType = Union[
    dse.Douse,
    dce.DicePool,
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

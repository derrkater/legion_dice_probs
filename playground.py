from pprint import pprint

import surge_conversion
from dice import RedAttackDouse

pprint(RedAttackDouse())
dice_pool = RedAttackDouse() + RedAttackDouse() + RedAttackDouse()
for i in range(3):
    dice_pool = dice_pool + RedAttackDouse()
pprint(dice_pool.most_common(5))
print(len(dice_pool))

pprint(surge_conversion.SurgeToHitConversion.apply(RedAttackDouse() + RedAttackDouse()))

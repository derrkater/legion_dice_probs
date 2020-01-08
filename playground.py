from pprint import pprint

from events import surge_conversion
from events import utility_events
from dice import RedAttackDouse, BlackAttackDouse

pprint(RedAttackDouse())
dice_pool = RedAttackDouse() + RedAttackDouse() + RedAttackDouse()
for i in range(3):
    dice_pool = dice_pool + RedAttackDouse()
pprint(dice_pool.most_common(5))
print(len(dice_pool))

pprint(surge_conversion.SurgeToHitConversion.apply(RedAttackDouse() + RedAttackDouse()))
pprint(surge_conversion.SurgeToHitConversion.apply(RedAttackDouse() + BlackAttackDouse()))
pprint(utility_events.RemoveColorsEvent.apply(surge_conversion.SurgeToHitConversion.apply(RedAttackDouse() + BlackAttackDouse())))

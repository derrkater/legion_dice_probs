from dice import AttackDicePool, AttackDouse, RedAttackDouse, BlackAttackDouse, WhiteAttackDouse
from roll_results import AttackRollResult


def calculate_attack_roll_probabilities(attack_dice_pool: AttackDicePool, attack_result: AttackRollResult):
    if attack_dice_pool.n_dice != attack_result.n_results:
        raise ValueError(f'Number of rolled results [{attack_result.n_results}] must match with total number of dice '
                         f'[{attack_dice_pool.n_dice}].')

    p = 0.
    for n_hits_on_red in range(attack_result.n_hit):
        for n_hits_on_black in range(attack_result.n_hit - n_hits_on_red):
            for n_hits_on_white in range(attack_result.n_hit - n_hits_on_red - n_hits_on_black):
                for n_blanks_on_red in range(attack_result.n_blank):
                    for n_blanks_on_black in range(attack_result.n_blank - n_blanks_on_red):
                        for n_blanks_on_white in range(attack_result.n_blank - n_blanks_on_red -n_blanks_on_black):
                            if (
                                    n_hits_on_red + n_hits_on_black + n_hits_on_white != attack_result.n_hit or
                                    n_blanks_on_red + n_blanks_on_black + n_blanks_on_white != attack_result.n_blank
                            ):
                                continue
                            p_element = RedAttackDouse.hit_prob ** n_hits_on_red
                            p_element += RedAttackDouse.blank_prob ** n_blanks_on_red
                            p_element += BlackAttackDouse.hit_prob ** n_hits_on_black
                            p_element += BlackAttackDouse.blank_prob ** n_blanks_on_black
                            p_element += WhiteAttackDouse.hit_prob ** n_hits_on_white
                            p_element += WhiteAttackDouse.blank_prob ** n_blanks_on_white

    p *= AttackDouse.crit_prob ** attack_result.n_crit * AttackDouse.surge_prob ** attack_result.n_surge

    return p

import fractions

from prob_dist_api import probability_distribution as pd


class StochasticState:
    def get_probability_distribution(self) -> pd.ProbabilityDistribution:
        return pd.ProbabilityDistribution(
            {
                self: fractions.Fraction(1)
            }
        )

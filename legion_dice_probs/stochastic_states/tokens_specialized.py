from legion_dice_probs.stochastic_states import token as tok
from legion_dice_probs.stochastic_states import tokens as toks


class AimToken(tok.Token):
    pass


class DodgeToken(tok.Token):
    pass


class SurgeToken(tok.Token):
    pass


class TokensAttack(toks.Tokens):
    @classmethod
    def from_attack_tokens(
            cls,
            n_aim: int = 0,
            n_surge: int = 0,
    ):
        return cls.from_tokens_list(
            [
                *[AimToken() for _ in range(n_aim)],
                *[SurgeToken() for _ in range(n_surge)],
            ]
        )


class TokensDefence(toks.Tokens):
    @classmethod
    def from_defence_tokens(
            cls,
            n_dodge: int = 0,
            n_surge: int = 0,
    ):
        return cls.from_tokens_list(
            [
                *[DodgeToken() for _ in range(n_dodge)],
                *[SurgeToken() for _ in range(n_surge)],
            ]
        )

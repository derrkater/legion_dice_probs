from typing import Optional

import dice_colors as col


class Symbol:
    def __init__(self, color: Optional[type(col.Color)] = None):
        self.color = color

    def __repr__(self):
        # return str(self.__class__.__name__)
        if self.color is None:
            return self.__class__.__name__
        return f'{self.__class__.__name__}_{self.color}'

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __hash__(self):
        return hash(f'{self.__class__.__name__}_{self.color}')


class Crit(Symbol):
    pass


class Hit(Symbol):
    pass


class Surge(Symbol):
    pass


class Block(Symbol):
    pass


class Blank(Symbol):
    pass

import dice_colors as col


class Symbol:
    def __init__(self, color: type(col.Color)):
        self.color = color

    def __repr__(self):
        return str(self.__class__.__name__)

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __hash__(self):
        return hash(self.__class__.__name__)


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

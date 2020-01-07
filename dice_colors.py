class Color:
    def __repr__(self):
        return str(self.__class__.__name__)

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __hash__(self):
        return hash(self.__class__.__name__)


class Red(Color):
    pass


class Black(Color):
    pass


class White(Color):
    pass

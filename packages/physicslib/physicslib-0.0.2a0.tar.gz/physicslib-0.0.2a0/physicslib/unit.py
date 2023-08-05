"""Unit class and unit constants."""

from physicslib import dimension
from physicslib.formating import superscripted


class Unit:
    """Unit of measurement."""

    def __init__(self, coefficient: float = 1, dim: dimension.Dimension = dimension.SCALAR):
        self.coefficient = coefficient
        self.dimension = dim.copy()

    def __repr__(self):
        return f"Unit({self.coefficient}, {repr(self.dimension)})"

    def __str__(self):
        string = ""
        if self.coefficient == -1:
            string += "-"
        elif self.coefficient != 1:
            string += str(self.coefficient)
            if self.dimension != dimension.SCALAR:
                string += "\u22C5"
        base_units = ["m", "kg", "s", "A", "K"]
        for i in range(5):
            if self.dimension.data[i] == 0:
                continue
            if string and string[-1].isalpha():
                string += "\u22C5"
            string += base_units[i]
            if self.dimension.data[i] != 1:
                string += superscripted(self.dimension.data[i])
        return string if string else "scalar_unit"

    def __mul__(self, other):
        return Unit(self.coefficient * other.coefficient, self.dimension * other.dimension)

    def __imul__(self, other):
        self.coefficient *= other.coefficient
        self.dimension *= other.dimension
        return self

    def __truediv__(self, other):
        return Unit(self.coefficient / other.coefficient, self.dimension / other.dimension)

    def __itruediv__(self, other):
        self.coefficient /= other.coefficient
        self.dimension /= other.dimension
        return self

    def __pow__(self, power):
        return Unit(self.coefficient ** power, self.dimension ** power)

    def __ipow__(self, power):
        self.coefficient **= power
        self.dimension **= power
        return self

    def __eq__(self, other):
        return self.coefficient == self.coefficient and self.dimension == other.dimension

    def copy(self):
        """Unit copy."""
        return Unit(self.coefficient, self.dimension)


# Base SI units
ONE = Unit()
METER = Unit(1, dimension.LENGTH)
SECOND = Unit(1, dimension.TIME)
KILOGRAM = Unit(1, dimension.MASS)
AMPER = Unit(1, dimension.AMPERAGE)
KELVIN = Unit(1, dimension.TEMPERATURE)

# Derived SI units
NEWTON = Unit(1, dimension.FORCE)
PASCAL = Unit(1, dimension.PRESSURE)
JOULE = Unit(1, dimension.WORK)

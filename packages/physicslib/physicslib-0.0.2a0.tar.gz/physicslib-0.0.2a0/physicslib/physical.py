"""Module with ScalarPhysical and VectorPhysical classes."""

from types import FunctionType

from physicslib import unit
from physicslib.vector import Vector


def unit_convert(func: FunctionType):
    """
    Decorator for Physical's methods.
    Converts second argument ('other') to 'other.to_unit(self.unit)'
    """
    def wrapper(self, other):
        return func(self, other.to_unit(self.unit))

    return wrapper


def convert_float(func):
    """
    Decorator for Physical's methods.
    If second argument ('other') is float or integer, converts it to ScalarPhysical.
    """
    def wrapper(self, other):
        if type(other) in (int, float):
            other = ScalarPhysical(other)
        return func(self, other)

    return wrapper


class ScalarPhysical:
    """Scalar physical quantity, like mass value or distance length."""
    def __init__(self, value: float = 0, unit_: unit.Unit = unit.ONE):
        self.value = value
        self.unit = unit_.copy()

    def __repr__(self):
        return f"ScalarPhysical({self.value}, {repr(self.unit)})"

    @convert_float
    @unit_convert
    def __add__(self, other):
        return ScalarPhysical(self.value + other.value, self.unit)

    @convert_float
    @unit_convert
    def __iadd__(self, other):
        self.value += other.value
        return self

    @convert_float
    def __mul__(self, other):
        if type(other) == VectorPhysical:
            return other * self
        return ScalarPhysical(self.value * other.value, self.unit * other.unit)

    @convert_float
    def __imul__(self, other):
        self.value *= other.value
        self.unit *= other.unit

    @convert_float
    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return ScalarPhysical(-self.value, self.unit)

    @convert_float
    @unit_convert
    def __sub__(self, other):
        return ScalarPhysical(self.value - other.value, self.unit)

    @convert_float
    @unit_convert
    def __isub__(self, other):
        self.value -= other.value
        return self

    @convert_float
    def __truediv__(self, other):
        return ScalarPhysical(self.value / other.value, self.unit / other.unit)

    @convert_float
    def __itruediv__(self, other):
        self.value /= other.value
        self.unit /= other.unit
        return self

    def __pow__(self, power):
        return ScalarPhysical(self.value ** power, self.unit ** power)

    def __ipow__(self, power):
        self.value **= power
        self.unit **= power

    @convert_float
    @unit_convert
    def __eq__(self, other):
        return self.value == other.value

    def to_unit(self, unit_: unit.Unit):
        """Equal physical quantity with new unit."""
        if self.unit.dimension != unit_.dimension:
            raise AttributeError("Bad unit dimension.")
        return ScalarPhysical(self.value * self.unit.coefficient / unit_.coefficient, unit_)

    def copy(self):
        return ScalarPhysical(self.value, self.unit)


class VectorPhysical:
    """Vector physical quantity, like velocity or force."""
    def __init__(self, value: Vector = Vector(), unit_: unit.Unit = unit.ONE):
        self.value = value
        self.unit = unit_

    def __repr__(self):
        return f"VectorPhysical({self.value}, {repr(self.unit)})"

    @unit_convert
    def __add__(self, other):
        return ScalarPhysical(self.value + other.value, self.unit)

    @unit_convert
    def __iadd__(self, other):
        self.value += other.value
        return self

    @convert_float
    def __mul__(self, other: ScalarPhysical):
        return VectorPhysical(self.value * other.value, self.unit * other.unit)

    @convert_float
    def __imul__(self, other: ScalarPhysical):
        self.value *= other.value
        self.unit *= other.unit
        return self

    @convert_float
    def __rmul__(self, other: ScalarPhysical):
        return self * other

    def __neg__(self):
        return VectorPhysical(-self.value, self.unit)

    @unit_convert
    def __sub__(self, other):
        return VectorPhysical(self.value - other.value, self.unit)

    @unit_convert
    def __isub__(self, other):
        self.value -= other.value
        return self

    @convert_float
    def __truediv__(self, other):
        return VectorPhysical(self.value / other.value, self.unit / other.unit)

    @convert_float
    def __itruediv__(self, other):
        self.value /= other.value
        self.unit /= other.unit
        return self

    @unit_convert
    def __eq__(self, other):
        return self.value == other.value

    def to_unit(self, unit_: unit.Unit):
        """Equal physical quantity with new unit."""
        if self.unit.dimension != unit_.dimension:
            raise AttributeError("Bad unit dimension.")
        return VectorPhysical(self.value * self.unit.coefficient / unit_.coefficient, unit_)

    def to_scalar(self) -> ScalarPhysical:
        """ScalarPhysical with value equal to the length of self.value and the same unit."""
        return ScalarPhysical(self.value.length(), self.unit)

    def x(self) -> ScalarPhysical:
        return ScalarPhysical(self.value.x(), self.unit)

    def y(self) -> ScalarPhysical:
        return ScalarPhysical(self.value.y(), self.unit)

    def z(self) -> ScalarPhysical:
        return ScalarPhysical(self.value.z(), self.unit)

    def x_vector(self):
        return VectorPhysical(self.value.x_vector(), self.unit)

    def y_vector(self):
        return VectorPhysical(self.value.y_vector(), self.unit)

    def z_vector(self):
        return VectorPhysical(self.value.z_vector(), self.unit)


Physical = ScalarPhysical


# constants
G = Physical(6.6743, unit.Unit(1e-11) * unit.METER ** 3 * unit.KILOGRAM ** -1 * unit.SECOND ** -2)
"""Gravity constant."""
EARTH_GRAVITY = VectorPhysical(Vector(0, 9.81), unit.METER * unit.SECOND ** -2)
"""Earth gravity acceleration."""

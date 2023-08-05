"""Module with Dimension class and dimension constants."""

from physicslib.formating import superscripted


class Dimension:
    """Physics dimension."""

    def __init__(
        self,
        length: int = 0,
        mass: int = 0,
        time: int = 0,
        amperage: int = 0,
        temperature: int = 0,
    ):
        self.data = [length, mass, time, amperage, temperature]

    def __repr__(self) -> str:
        string = "Dimension("
        for i in range(5):
            string += f"{self.data[i]}, "
        return string[:-2] + ")"

    def __str__(self) -> str:
        name_chars = ["L", "M", "T", "I", "\u0398"]
        string = ""
        for i in range(5):
            if self.data[i] == 0:
                continue
            string += name_chars[i]
            if self.data[i] != 1:
                string += superscripted(self.data[i])
        return string if string else "scalar"

    def __mul__(self, other):
        return Dimension(*(self.data[i] + other.data[i] for i in range(5)))

    def __imul__(self, other):
        for i in range(5):
            self.data[i] += other.data[i]
        return self

    def __truediv__(self, other):
        return Dimension(*(self.data[i] - other.data[i] for i in range(5)))

    def __itruediv__(self, other):
        for i in range(5):
            self.data[i] -= other.data[i]
        return self

    def __pow__(self, power):
        return Dimension(*(self.data[i] * power for i in range(5)))

    def __ipow__(self, power):
        for i in range(5):
            self.data[i] *= power
        return self

    def __eq__(self, other) -> bool:
        return self.data == other.data

    def copy(self):
        """Copy object."""
        return Dimension(*self.data)


# Base dimensions
SCALAR = Dimension()
LENGTH = Dimension(length=1)
TIME = Dimension(time=1)
MASS = Dimension(mass=1)
AMPERAGE = Dimension(amperage=1)
TEMPERATURE = Dimension(temperature=1)

# Derived dimensions
SQUARE = LENGTH ** 2
VOLUME = LENGTH ** 3
DENSITY = MASS / VOLUME
VELOCITY = LENGTH / TIME
ACCELERATION = VELOCITY / TIME
FORCE = MASS * ACCELERATION
PRESSURE = FORCE / SQUARE
MOMENTUM = VELOCITY * MASS
WORK = FORCE * LENGTH

from typing import Optional, List

from physicslib import unit

from physicslib.physical import Physical, VectorPhysical, EARTH_GRAVITY
from physicslib.vector import Vector


class PhysicsBody:
    # TODO this class better
    """Simple body with Newton mechanic laws."""

    def __init__(
        self,
        mass: Optional[Physical] = None,
        volume: Optional[Physical] = None,
        initial_speed: VectorPhysical = VectorPhysical(),
        gravity_acceleration: VectorPhysical = EARTH_GRAVITY
    ):
        self.mass = mass
        self.volume = volume
        self.speed = initial_speed
        self.gravity_acceleration = gravity_acceleration
        self.forces: List[VectorPhysical] = []

    def density(self) -> Optional[Physical]:
        """Density of body, if its mass and volume are defined."""
        if self.mass is None or self.volume is None:
            return None
        return self.mass / self.volume

    def add_force(self, force: VectorPhysical) -> None:
        self.forces.append(force)

    def force_sum(self) -> VectorPhysical:
        forces_sum = VectorPhysical(Vector(), unit.NEWTON)
        if self.mass is not None:
            forces_sum += self.mass * self.gravity_acceleration
        return forces_sum

    def acceleration(self) -> Optional[VectorPhysical]:
        """Acceleration of body, if it is possible to calculate."""
        force_sum = self.force_sum()
        if self.mass is None or self.mass.value == 0:
            if force_sum.value == Vector():
                return self.gravity_acceleration
            return None
        return force_sum / self.mass

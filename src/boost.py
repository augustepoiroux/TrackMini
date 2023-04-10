from dataclasses import dataclass
from abc import ABC

from pymunk import Vec2d
import pymunk

from material import Material
from physic_object import PhysicObject


@dataclass(kw_only=True)
class BoostMaterial(Material, ABC):
    power: float


@dataclass(kw_only=True)
class YellowBoostMaterial(BoostMaterial):
    color: tuple[int, int, int, int] = (255, 255, 0, 255)
    friction: float = 0.9
    elasticity: float = 0.6
    power: float = 10


@dataclass(kw_only=True)
class RedBoostMaterial(BoostMaterial):
    color: tuple[int, int, int, int] = (255, 0, 0, 255)
    friction: float = 0.9
    elasticity: float = 0.6
    power: float = 15


class Boost(PhysicObject):
    def __init__(
        self,
        material: BoostMaterial,
        position: Vec2d,
        angle: float = 0.0,
        width: float = 25.0,
        length: float = 25.0,
    ) -> None:
        self.material = material
        self.width = width
        self.length = length

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.body.angle = angle

        self.shape = pymunk.Poly.create_box(self.body, (self.length, self.width), 0.0)


if __name__ == "__main__":
    boost = Boost(material=YellowBoostMaterial(), position=Vec2d(0, 0))
    print(boost.material)
    print(boost.body.position)
    print(boost.width)
    print(boost.length)

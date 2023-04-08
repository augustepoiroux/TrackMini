from dataclasses import dataclass

from material import Material


# to put in material.py?
@dataclass(kw_only=True)
class BoostMaterial(Material):
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


class Boost:
    def __init__(
        self,
        material: Material,
        position: tuple[float, float],
        width: float = 25.0,
        length: float = 25.0,
    ) -> None:
        self.material = material
        self.position = position
        self.width = width
        self.length = length


if __name__ == "__main__":
    boost = Boost(material=YellowBoostMaterial(), position=(0, 0))
    print(boost.material)
    print(boost.position)
    print(boost.width)
    print(boost.length)

from material import Material
import pymunk

from physic_object import PhysicObject


class Road(PhysicObject):
    def __init__(
        self,
        material: Material,
        position: tuple[float, float],
        angle: float = 0.0,
        width: float = 32.0,
        length: float = 32.0,
    ) -> None:
        self.material = material
        self.width = width
        self.length = length

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.body.angle = angle

        self.shape = pymunk.Poly.create_box(self.body, (self.length, self.width), 0.0)

    def add(self, space: pymunk.Space) -> None:
        space.add(self.body, self.shape)


if __name__ == "__main__":
    from material import Concrete

    road = Road(material=Concrete(), position=(0, 0))
    print(road.material)
    print(road.body.position)
    print(road.width)
    print(road.length)

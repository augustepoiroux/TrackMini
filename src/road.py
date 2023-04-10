from material import Material
import pymunk

from physic_object import PhysicObject


class Road(PhysicObject):
    def __init__(
        self,
        material: Material,
        position: tuple[float, float],
        angle: float = 0.0,
        width: float = 25.0,
        length: float = 50.0,
    ) -> None:
        self.material = material
        self.width = width
        self.length = length

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.body.angle = angle

        self.shape = pymunk.Poly.create_box(self.body, (self.length, self.width), 0.0)


if __name__ == "__main__":
    from material import Concrete

    road = Road(material=Concrete(), position=(0, 0))
    print(road.material)
    print(road.body.position)
    print(road.width)
    print(road.length)

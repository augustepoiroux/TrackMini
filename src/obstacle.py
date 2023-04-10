from material import Material
from physic_object import PhysicObject
import pymunk


class Obstacle(PhysicObject):
    def __init__(
        self,
        material: Material,
        position: tuple[float, float],
        angle: float = 0.0,
        width: float = 10.0,
        length: float = 10.0,
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

    obstacle = Obstacle(material=Concrete(), position=(0, 0))
    print(obstacle.material)
    print(obstacle.body.position)
    print(obstacle.width)
    print(obstacle.length)

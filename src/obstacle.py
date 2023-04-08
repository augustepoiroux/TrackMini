from material import Material


class Obstacle:
    def __init__(
        self,
        material: Material,
        position: tuple[float, float],
        width: float = 10.0,
        length: float = 10.0,
    ) -> None:
        self.material = material
        self.position = position
        self.width = width
        self.length = length


if __name__ == "__main__":
    from material import Concrete

    obstacle = Obstacle(material=Concrete(), position=(0, 0))
    print(obstacle.material)
    print(obstacle.position)
    print(obstacle.width)
    print(obstacle.length)

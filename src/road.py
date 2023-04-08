from material import Material


class Road:
    def __init__(
        self,
        material: Material,
        position: tuple[float, float],
        width: float = 25.0,
        length: float = 50.0,
    ) -> None:
        self.material = material
        self.position = position
        self.width = width
        self.length = length


if __name__ == "__main__":
    from material import Concrete

    road = Road(material=Concrete(), position=(0, 0))
    print(road.material)
    print(road.position)
    print(road.width)
    print(road.length)

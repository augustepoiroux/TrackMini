from abc import ABC
from dataclasses import dataclass


@dataclass
class Material(ABC):
    color: tuple[int, int, int, int]
    friction: float
    elasticity: float


@dataclass(kw_only=True)
class Concrete(Material):
    color: tuple[int, int, int, int] = (200, 200, 200, 255)
    friction: float = 0.75
    elasticity: float = 0.1


@dataclass(kw_only=True)
class Grass(Material):
    color: tuple[int, int, int, int] = (100, 255, 100, 255)
    friction: float = 0.5
    elasticity: float = 0.3


@dataclass(kw_only=True)
class Dirt(Material):
    color: tuple[int, int, int, int] = (150, 150, 25, 255)
    friction: float = 0.6
    elasticity: float = 0.2


@dataclass(kw_only=True)
class Ice(Material):
    color: tuple[int, int, int, int] = (255, 200, 200, 255)
    friction: float = 0.2
    elasticity: float = 0.15


@dataclass(kw_only=True)
class Plastic(Material):
    color: tuple[int, int, int, int] = (255, 100, 100, 255)
    friction: float = 0.9
    elasticity: float = 0.6


@dataclass(kw_only=True)
class Rubber(Material):
    color: tuple[int, int, int, int] = (255, 100, 100, 255)
    friction: float = 0.9
    elasticity: float = 0.6

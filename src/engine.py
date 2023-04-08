from dataclasses import dataclass

import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
from car import PhysicCar
from pymunk.vec2d import Vec2d


@dataclass
class Action:
    # values are normalized to [-1, 1]
    wheel_angle: float
    throttle: float

    def __post_init__(self) -> None:
        self.wheel_angle = float(np.clip(self.wheel_angle, -1, 1))
        self.throttle = float(np.clip(self.throttle, -1, 1))


class CoreEngine:
    def __init__(self, dt: float) -> None:
        self.dt = dt

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        self.car = PhysicCar(position=Vec2d(100, 100))
        self.space.add(self.car.body, self.car.shape)

    def update(self, action: Action) -> None:
        self.car.update(throttle=action.throttle, wheel_angle=action.wheel_angle)

        # update the world
        self.space.step(self.dt)

    def draw(self, surface: pygame.Surface) -> None:
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(surface))

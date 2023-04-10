from dataclasses import dataclass

import numpy as np
import pymunk
from car import PhysicCar

from physic_object import PhysicObject, UpdatablePhysicObject


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
        self.space.damping = 0.9

        self.updatable_objects: list[UpdatablePhysicObject] = []

    def add(self, physic_object: PhysicObject) -> None:
        self.space.add(physic_object.body, physic_object.shape)
        if isinstance(physic_object, UpdatablePhysicObject):
            self.updatable_objects.append(physic_object)

    def update(self, action: Action) -> None:
        for obj in self.updatable_objects:
            if isinstance(obj, PhysicCar):
                obj.update(throttle=action.throttle, wheel_angle=action.wheel_angle)
            else:
                raise NotImplementedError

        # update the world
        self.space.step(self.dt)

    def draw(self, draw_options) -> None:
        self.space.debug_draw(draw_options)

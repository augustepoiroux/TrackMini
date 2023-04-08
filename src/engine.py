from dataclasses import dataclass

import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
from gui import *


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

        self._instantiate_car()

    def _instantiate_car(self) -> None:
        # define constants
        self.car_mass = 1
        self.car_width = 30
        self.car_length = 60
        self.car_radius = Vec2d(self.car_width, self.car_width).length
        self.car_speed = 0
        self.car_acceleration = 50
        self.car_brake = 200
        self.car_friction = 0.8
        self.car_rotation_speed = 3

        self.car_body = pymunk.Body()
        self.car_body.position = Vec2d(self.car_radius, self.car_radius)

        shape = pymunk.Poly.create_box(self.car_body, (self.car_length, self.car_width), 0.0)
        shape.mass = self.car_mass
        shape.friction = 0.7
        self.space.add(self.car_body, shape)

        for s in self.car_body.shapes:
            s.color = car_color

    def update(self, action: Action) -> None:
        # kill lateral velocity
        current_right_normal = self.car_body.local_to_world((1, 0))
        current_lateral_velocity = current_right_normal.dot(self.car_body.velocity) * current_right_normal
        self.car_body.apply_impulse_at_world_point(
            0.0001 * self.car_body.mass * -current_lateral_velocity, self.car_body.position
        )

        # apply longitudinal force
        acceleration_scalar = action.throttle * (self.car_acceleration if action.throttle > 0 else self.car_brake)
        self.car_body.apply_force_at_local_point(
            self.car_body.mass * acceleration_scalar * self.car_body.rotation_vector,
        )

        # update the world
        self.space.step(self.dt)

    def draw(self, surface: pygame.Surface) -> None:
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(surface))

"""
Heavily inspired by: http://www.iforce2d.net/b2dtut/top-down-car.
"""

import pymunk
from gui import car_color, tire_color
from pymunk import Vec2d
from physic_object import UpdatablePhysicObject

from utils import apply_angular_impulse, apply_torque


class PhysicCar(UpdatablePhysicObject):
    def __init__(self, position: Vec2d) -> None:
        # define constants
        self.mass = 1
        self.width = 30
        self.length = 60
        self.radius = Vec2d(self.width, self.width).length
        self.acceleration = 50
        self.brake = 200
        self.friction = 0.8

        self.body = pymunk.Body()
        self.body.position = position

        self.shape = pymunk.Poly.create_box(self.body, (self.length, self.width), 0.0)
        self.shape.mass = self.mass
        self.shape.friction = self.friction

        for s in self.body.shapes:
            s.color = car_color

    def update(self, throttle: float, wheel_angle: float) -> None:
        # apply longitudinal force
        acceleration_scalar = throttle * (self.acceleration if throttle > 0 else self.brake)
        self.body.apply_force_at_local_point(
            self.body.mass * acceleration_scalar * self.body.rotation_vector,
        )


class PhysicTire(UpdatablePhysicObject):
    def __init__(self, position: Vec2d, angle: float) -> None:
        self.position = position
        self.angle = angle
        self.mass = 1
        self.length = 100
        self.width = 30
        self.angular_friction = 0.1
        self.drag = 1
        self.max_lateral_impulse = 0.1
        self.current_traction = 1  # to be updated depending on the surface

        self.turn_force = 5000
        self.max_drive_force = 150

        self.body = pymunk.Body()
        self.body.position = position
        self.body.angle = angle

        self.shape = pymunk.Poly.create_box(self.body, (self.length, self.width), 0.0)
        self.shape.mass = self.mass

        for s in self.body.shapes:
            s.color = tire_color

    def update(self, throttle, wheel_angle) -> None:
        self.update_friction()
        self.update_drive(throttle)
        self.update_turn(wheel_angle)

    def update_friction(self) -> None:
        # kill lateral velocity
        impulse = self.body.mass * -self.get_lateral_velocity()
        if impulse.length > self.max_lateral_impulse:
            impulse *= self.max_lateral_impulse / impulse.length
        self.body.apply_impulse_at_world_point(impulse=impulse, point=self.body.position)

        # reduce angular velocity
        apply_angular_impulse(
            body=self.body,
            impulse=self.angular_friction * self.body.moment * -self.body.angular_velocity,
            dist=self.length,
        )

        # apply drag
        self.body.apply_force_at_world_point(-self.drag * self.body.velocity, self.body.position)

    def update_drive(self, throttle):
        force = throttle * self.max_drive_force
        self.body.apply_force_at_world_point(force * self.body.rotation_vector, self.body.position)

    def update_turn(self, wheel_angle):
        apply_torque(body=self.body, torque=wheel_angle * self.turn_force, dist=self.length)

    def get_lateral_velocity(self) -> Vec2d:
        return self.body.velocity.projection(self.body.rotation_vector.perpendicular())

    def get_forward_velocity(self) -> Vec2d:
        return self.body.velocity.projection(self.body.rotation_vector)

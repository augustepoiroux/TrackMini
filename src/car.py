"""
Heavily inspired by: http://www.iforce2d.net/b2dtut/top-down-car.
"""

import pymunk
from gui import car_color, tire_color
from pymunk import Vec2d
from physic_object import UpdatablePhysicObject

from utils import apply_angular_impulse, apply_torque


class PhysicCar(UpdatablePhysicObject):
    def __init__(self, position: Vec2d, angle: float) -> None:
        # define constants
        self.mass = 1000
        self.width = 150
        self.length = 300
        self.friction = 0.8

        self.body = pymunk.Body()
        self.body.position = position
        self.body.angle = angle

        self.shape = pymunk.Poly.create_box(self.body, (self.length, self.width), 0.0)
        self.shape.mass = self.mass
        self.shape.friction = self.friction

        for s in self.body.shapes:
            s.color = car_color

        self.tires = {
            "front_left": PhysicTire(
                position=self.body.position + Vec2d(self.length / 2.0, -self.width / 2.0 - PhysicTire.width),
                angle=angle,
            ),
            "front_right": PhysicTire(
                position=self.body.position + Vec2d(self.length / 2.0, self.width / 2.0 + PhysicTire.width),
                angle=angle,
            ),
            "back_left": PhysicTire(
                position=self.body.position + Vec2d(-self.length / 2.0, -self.width / 2.0 - PhysicTire.width),
                angle=angle,
            ),
            "back_right": PhysicTire(
                position=self.body.position + Vec2d(-self.length / 2.0, self.width / 2.0 + PhysicTire.width),
                angle=angle,
            ),
        }

        self.joints = [
            pymunk.PinJoint(self.tires["back_left"].body, self.body, (0, 0), (0, 0)),
            pymunk.constraints.RotaryLimitJoint(self.tires["back_left"].body, self.body, 0, 0),
            pymunk.constraints.PivotJoint(
                self.tires["back_left"].body, self.body, self.tires["back_left"].body.position
            ),
            pymunk.PinJoint(self.tires["back_right"].body, self.body, (0, 0), (0, 0)),
            pymunk.constraints.RotaryLimitJoint(self.tires["back_right"].body, self.body, 0, 0),
            pymunk.constraints.PivotJoint(
                self.tires["back_right"].body, self.body, self.tires["back_right"].body.position
            ),
            pymunk.PinJoint(self.tires["front_left"].body, self.body, (0, 0), (0, 0)),
            pymunk.constraints.PivotJoint(
                self.tires["front_left"].body, self.body, self.tires["front_left"].body.position
            ),
            pymunk.PinJoint(self.tires["front_right"].body, self.body, (0, 0), (0, 0)),
            pymunk.constraints.PivotJoint(
                self.tires["front_right"].body, self.body, self.tires["front_right"].body.position
            ),
        ]

    def add(self, space: pymunk.Space) -> None:
        space.add(self.body, self.shape)
        space.add(*self.joints)
        for tire in self.tires.values():
            tire.add(space)

    def update(self, throttle: float, wheel_angle: float) -> None:
        for tire_name, tire in self.tires.items():
            if "front" in tire_name:
                tire.update(throttle, wheel_angle)
            else:
                tire.update(throttle, 0)


class PhysicTire(UpdatablePhysicObject):
    mass: float = 7
    length: float = 100
    width: float = 30
    angular_friction: float = 0.1
    drag: float = 1
    max_lateral_impulse: float = 100
    # current_traction: float = 1  # to be updated depending on the surface
    turn_force: float = 50000
    max_drive_force: float = 15000

    def __init__(self, position: Vec2d, angle: float) -> None:
        self.position = position
        self.angle = angle

        self.body = pymunk.Body()
        self.body.position = position
        self.body.angle = angle

        self.shape = pymunk.Poly.create_box(self.body, (self.length, self.width), 0.0)
        self.shape.mass = self.mass

        for s in self.body.shapes:
            s.color = tire_color

    def add(self, space: pymunk.Space) -> None:
        space.add(self.body, self.shape)

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

import pymunk
from gui import car_color, tire_color
from pymunk.vec2d import Vec2d


class PhysicCar:
    """http://www.iforce2d.net/b2dtut/top-down-car."""

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
        # kill lateral velocity
        current_right_normal = self.body.rotation_vector.rotated_degrees(90)
        current_lateral_velocity = current_right_normal.dot(self.body.velocity) * current_right_normal
        self.body.apply_impulse_at_local_point(0.0001 * self.body.mass * -current_lateral_velocity)

        # apply longitudinal force
        acceleration_scalar = throttle * (self.acceleration if throttle > 0 else self.brake)
        self.body.apply_force_at_local_point(
            self.body.mass * acceleration_scalar * self.body.rotation_vector,
        )


class PhysicTire:
    def __init__(self, position: Vec2d, angle: float) -> None:
        self.position = position
        self.angle = angle
        self.mass = 1
        self.length = 5
        self.width = 2
        self.angular_friction = 0.1
        self.drag = 2

        self.body = pymunk.Body()

        self.shape = pymunk.Poly.create_box(self.body, (self.length, self.width), 0.0)
        self.shape.mass = self.mass

        for s in self.body.shapes:
            s.color = tire_color

    def update(self) -> None:
        self.update_friction()

    def update_friction(self) -> None:
        # kill lateral velocity
        self.body.apply_impulse_at_local_point(self.body.mass * -self.get_lateral_velocity())

        # reduce angular velocity
        angular_impulse = self.angular_friction * self.body.moment * -self.body.angular_velocity
        self.body.apply_impulse_at_local_point(
            impulse=angular_impulse / self.length,  # TODO: is this correct?
            point=Vec2d(self.length, 0).rotated(self.body.angle),
        )

        # apply drag
        drag_force_scalar = -self.drag * self.body.velocity.length
        self.body.apply_force_at_local_point(drag_force_scalar * self.body.velocity)

    def get_lateral_velocity(self) -> Vec2d:
        current_right_normal: Vec2d = self.body.rotation_vector.rotated_degrees(90)
        return current_right_normal.dot(self.body.velocity) * current_right_normal

import pymunk
from pymunk.vec2d import Vec2d


def apply_torque(body: pymunk.Body, torque: float, dist: float = 1.0):
    body.apply_force_at_local_point(
        force=Vec2d(0, torque / dist),
        point=Vec2d(dist, 0),
    )


def apply_angular_impulse(body: pymunk.Body, impulse: float, dist: float = 1.0):
    body.apply_impulse_at_local_point(
        impulse=Vec2d(0, impulse / dist),  # TODO: is this correct?
        point=Vec2d(dist, 0),
    )

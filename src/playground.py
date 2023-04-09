import pygame
import pymunk
import pymunk.pygame_util
from car import PhysicCar, PhysicTire
from pymunk.vec2d import Vec2d

if __name__ == "__main__":
    # fps handlings
    fps = 60
    dt = 1 / fps

    # initialization
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, 0)

    # Add objects here
    tire = PhysicTire(position=Vec2d(screen_width / 2.0, screen_height / 2.0), angle=0)
    space.add(tire.body, tire.shape)
    car = PhysicCar(position=Vec2d(screen_width / 3.0, screen_height / 2.0))
    space.add(car.body, car.shape)

    ### ALL SETUP DONE

    selected = None
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # handle events
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        mouse_button = pygame.mouse.get_pressed()
        mouse_body.position = pygame.mouse.get_pos()

        # handle key presses
        if keys[pygame.K_ESCAPE]:
            running = False

        throttle = keys[pygame.K_UP] - keys[pygame.K_DOWN]
        wheel_angle = 0

        # handle mouse presses
        if mouse_button[0]:
            mouse_pos = pygame.mouse.get_pos()
            mouse_body.position = Vec2d(*mouse_pos)
            if selected is None:
                hit = space.point_query(mouse_body.position, 0, pymunk.ShapeFilter())
                if hit != [] and hit[0].shape is not None:
                    body = hit[0].shape.body
                    rest_length = mouse_body.position.get_distance(body.position)
                    stiffness = 100
                    damping = 100
                    selected = pymunk.DampedSpring(mouse_body, body, (0, 0), (0, 0), rest_length, stiffness, damping)
                    space.add(selected)
        elif selected is not None:
            space.remove(selected)
            selected = None

        tire.update()
        car.update(throttle=throttle, wheel_angle=wheel_angle)
        space.step(dt)

        # draw
        screen.fill((0, 0, 0))
        space.debug_draw(draw_options)
        pygame.display.set_caption(f"Playground - fps: {clock.get_fps():.1f}")

        pygame.display.flip()
        clock.tick(fps)

import pygame
import pymunk
import pymunk.pygame_util
from car import PhysicCar
from pymunk import Vec2d
from gui import background_color

if __name__ == "__main__":
    # fps handlings
    fps = 60
    dt = 1 / fps

    # initialization
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, 0)

    # Add objects here
    car = PhysicCar(position=Vec2d(screen_width / 2, screen_height / 2), angle=0)
    car.add(space)

    ### ALL SETUP DONE

    mouse_springs = []
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

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
        wheel_angle = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

        # handle mouse presses
        if mouse_button[0]:
            mouse_pos = pygame.mouse.get_pos()
            mouse_body.position = Vec2d(*mouse_pos)
            if mouse_springs == []:
                hit = space.point_query(mouse_body.position, 0, pymunk.ShapeFilter())
                if hit != [] and hit[0].shape is not None:
                    body = hit[0].shape.body
                    rest_length = mouse_body.position.get_distance(body.position)
                    stiffness = 1000
                    damping = 10

                    mouse_springs.append(
                        pymunk.DampedSpring(mouse_body, body, (0, 0), (0, 0), rest_length, stiffness, damping),
                    )

                    stiffness = 125000.0
                    damping = 6000.0
                    mouse_springs.append(pymunk.DampedRotarySpring(mouse_body, body, 0, stiffness, damping))

                    for spring in mouse_springs:
                        space.add(spring)
        elif mouse_springs != []:
            for spring in mouse_springs:
                space.remove(spring)
            mouse_springs = []

        r = 1
        for _ in range(r):
            car.update(throttle=throttle, wheel_angle=wheel_angle)
            space.step(dt / r)

        # draw
        screen.fill(background_color)
        space.debug_draw(draw_options)
        pygame.display.set_caption(f"Playground - fps: {clock.get_fps():.1f}")
        pygame.display.flip()

        clock.tick(fps)

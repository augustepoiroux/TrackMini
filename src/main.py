import pygame
from pymunk import Vec2d
import pymunk.pygame_util
from engine import Action, CoreEngine
from gui import background_color
from car import PhysicCar

if __name__ == "__main__":
    # fps handlings
    fps = 60

    # initialization
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    clock = pygame.time.Clock()

    # add objects here
    engine = CoreEngine(dt=1 / fps)
    engine.add(PhysicCar(position=Vec2d(100, 100)))

    # handle events
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # handle key presses
        keys = pygame.key.get_pressed()

        # quit
        if keys[pygame.K_ESCAPE]:
            running = False

        action = Action(
            throttle=keys[pygame.K_UP] - keys[pygame.K_DOWN],
            wheel_angle=0,
        )

        # update the world
        engine.update(action)

        # background
        screen.fill(background_color)

        # drawings
        engine.draw(draw_options)

        pygame.display.flip()

        clock.tick(fps)
        pygame.display.set_caption(f"TrackMini - fps: {clock.get_fps():.1f}")

import pygame
from engine import Action, CoreEngine
from gui import background_color

if __name__ == "__main__":
    # fps handlings
    fps = 60
    engine = CoreEngine(dt=1 / fps)

    # initialization
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

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
        engine.draw(screen)

        pygame.display.flip()

        clock.tick(fps)
        pygame.display.set_caption(f"TrackMini - fps: {clock.get_fps():.1f}")

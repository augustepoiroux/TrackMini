import pygame

from engine import CoreEngine, Action

if __name__ == "__main__":
    fps = 60
    engine = CoreEngine(dt=1 / fps)
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TrackMini")
    clock = pygame.time.Clock()

    # Handle events
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        # Handle key presses
        keys = pygame.key.get_pressed()
        action = Action(
            throttle=keys[pygame.K_UP] - keys[pygame.K_DOWN],
            wheel_angle=0,
        )
        engine.update(action)

        screen.fill(pygame.Color("black"))
        engine.draw(screen)
        pygame.display.flip()

        clock.tick(fps)

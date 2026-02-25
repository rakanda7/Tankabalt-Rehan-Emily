import sys

import pygame
import pygame.locals
import random


WIDTH, HEIGHT = 900, 650

class Character:
    ...


class Ground:
    
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.x = 920
        self.vx = -2
        self.width = random.uniform(50,250)

    def update(self) -> None:
        self.x += self.vx
        if self.x + self.width < 0:
            self.kill()

    def display(self) -> None:
        pygame.draw.rectangle(self.screen, "#FF0000", (self.x, 600, self.width, 50))

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    Ground(screen)

    while True:
        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
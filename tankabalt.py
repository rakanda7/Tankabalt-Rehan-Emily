import sys

import pygame
import pygame.locals
import random
import time


WIDTH, HEIGHT = 900, 650

class Character:
    ...


class Ground:
    
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.x = 920
        self.vx = -5
        self.width = random.uniform(50,250)

    def update(self) -> None:
        self.x += self.vx
        if self.x + self.width < 0:
            self.kill()

    def display(self) -> None:
        pygame.draw.rect(self.screen, "#FF0000", (self.x, 600, self.width, 50))

class Obstacle:
    ...

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    ground = [Ground(screen) for i in range(1,100)]

    while True:
        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        for g in ground:
            g.update()
            g.display()

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
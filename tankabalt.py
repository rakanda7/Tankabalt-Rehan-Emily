import sys

import pygame
import pygame.locals
import random
import time


WIDTH, HEIGHT = 900, 650

class Character:
    def __init__(self, screen: pygame.Surface, y: int) -> None:
        self.screen = screen
        self.radius = 15
        self.velocity = 5
        self.color = "#FEFEFE" 
        self.x = 50
        self.y = y
    
    def motion(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.y += self.velocity
        
        top = self.radius
        bottom = self.screen.get_height() - self.radius
        
        # ball doesn't move off the screen
        if self.y < top:
            self.y = top
        if self.y > bottom:
            self.y = bottom
    
    def update(self) -> None:
        self.motion()

    def display(self) -> None:
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)



class Ground:
    
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.x = 920
        self.vx = -5
        self.width = random.uniform(50,250)

    def update(self) -> None:
        self.x += self.vx
        if self.x + self.width < 0:
            del(self)

    def display(self) -> None:
        pygame.draw.rect(self.screen, "#FF0000", (self.x, 600, self.width, 50))

class Obstacle:
    ...

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    ground = Ground(screen)
    ball = Character(screen, 300)

    while True:
        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        for g in ground:
            g.update()
            g.display()

        ball.update()
        ball.display()

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
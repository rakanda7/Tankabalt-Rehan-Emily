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
        self.color = "#FEFEFE" 
        
        self.x = 50

        self.ground_y = 500
        self.y = 500
        self.vy = 0
        self.jump_velocity = 18
        self.gravity = 1
        self.on_ground = True

        self.prev_up_pressed = False

    
    def motion(self) -> None:
        keys = pygame.key.get_pressed()
        up_pressed = keys[pygame.K_UP]

        if up_pressed and self.on_ground and not self.prev_up_pressed:
            self.vy = -self.jump_velocity
            self.on_ground = False
        
        self.prev_up_pressed = up_pressed

        # apply gravity and move
        self.vy += self.gravity
        self.y += self.vy

        # ground collision
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.vy = 0
            self.on_ground = True

    
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
        pygame.draw.rect(self.screen, "#FF0000", (self.x, 500, self.width, 50))

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

        ground.update()
        ground.display()

        ball.update()
        ball.display()

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
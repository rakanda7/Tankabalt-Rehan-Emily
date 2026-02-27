import sys

import pygame
import pygame.locals
import random
import time


WIDTH, HEIGHT = 900, 650

class Character:
    def __init__(self, screen: pygame.Surface, y: int, g_one, g_two, g_three) -> None:
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

        self.extra_jumps = 1
        self.jumps_left = 1

        self.prev_up_pressed = False

        self.g_one = g_one
        self.g_two = g_two
        self.g_three = g_three

    def jump(self) -> None:
        self.vy = -self.jump_velocity
        self.on_ground = False
    
    def motion(self) -> None:
        keys = pygame.key.get_pressed()
        up_pressed = keys[pygame.K_UP]
        just_pressed_up = up_pressed and not self.prev_up_pressed
        
        self.prev_up_pressed = up_pressed

        # jumping (re-jumps mid-air if up pressed)
        if just_pressed_up:
            if self.on_ground:
                self.jump()
            elif self.jumps_left > 0:
                self.jump()
                self.jumps_left -= 1

        # apply gravity and move
        self.vy += self.gravity
        self.y += self.vy

        # ground collision
        if ( 
            self.x >= self.g_one.x and 
            self.x <= (self.g_one.x + self.g_one.width) and
            self.x >= self.g_two.x and 
            self.x <= (self.g_two.x + self.g_two.width) and
            self.x >= self.g_three.x and 
            self.x <= (self.g_three.x + self.g_three.width)
        ):
            self.y += self.gravity
            self.on_ground = True
            self.jumps_left = self.extra_jumps

    
    def update(self) -> None:
        self.motion()


    def display(self) -> None:
        pygame.draw.circle(self.screen, self.color, (self.x, self.y - self.radius), self.radius)


class Ground:
    
    def __init__(self, screen: pygame.Surface, x:int) -> None:
        self.screen = screen
        self.x = x
        self.vx = -5
        self.width = random.uniform(180,400)

    def update(self) -> None:
        self.x += self.vx
        if self.x + self.width < 0:
            self.width = random.uniform(180,400)
            self.x = 800 + self.width

    def display(self) -> None:
        pygame.draw.rect(self.screen, "#FF0000", (self.x, 500, self.width, 50))

class Obstacle:
    ...

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    g_one = Ground(screen, 0)
    g_two = Ground(screen, 500)
    g_three = Ground(screen, 900)
    ball = Character(screen, 300)

    while True:
        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        g_one.update()
        g_one.display()
        g_two.update()
        g_two.display()
        g_three.update()
        g_three.display()

        ball.update()
        ball.display()

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
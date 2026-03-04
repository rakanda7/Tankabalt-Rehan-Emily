import sys

import pygame
import pygame.locals
import random
import time


WIDTH, HEIGHT = 900, 650

class Character:
    def __init__(self, screen: pygame.Surface, y: int, grounds) -> None:
        self.screen = screen
        self.radius = 15
        self.color = "#FEFEFE"
        self.x = 50
        self.ground_y = 500
        self.y = 500
        self.vy = 0
        self.jump_velocity = 18
        self.gravity = 1

        self.extra_jumps = 1
        self.jumps_left = 1

        self.prev_up_pressed = False
        self.prev_space_pressed = False

        self.bullets: list[Bullet] = []

        self.bullet_count = 10
        self.bullet_spacing = 12
        self.bullet_velocity = 15.0
        self.bullet_radius = 5

        self.grounds = grounds

        self.health = 9

    def jump(self) -> None:
        self.vy = -self.jump_velocity

    def shoot_bullet(self) -> None:
        bullet_x = self.x + self.radius + self.bullet_radius * 2
        bullet_y = self.y - self.radius

        self.bullets.append(Bullet(self.screen, bullet_x, bullet_y))
        
    def motion(self) -> None:
        self.on_ground = False
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
        self.jumps_left = self.extra_jumps

        # apply gravity and move
        prev_y = self.y
        self.vy += self.gravity
        self.y += self.vy

        # ceiling for ball
        if self.y < 2 * self.radius:
            self.y = 2 * self.radius
            if self.vy < 0:
                self.vy = 0
        
        # press space bar to shoot bullets
        space_pressed = keys[pygame.K_SPACE]
        just_pressed_space = space_pressed and not self.prev_space_pressed
        self.prev_space_pressed = space_pressed

        if just_pressed_space:
            self.shoot_bullet( )

        # ground collision
        
        for g in self.grounds:
            if (
                self.x >= g.x and
                self.x <= g.x + g.width and
                self.y >= 500 and
                prev_y <= 500 and
                self.vy > 0
            ):
                self.y = 500
                self.vy = 0
                self.on_ground = True
                break

    # reset 
    def reset(self) -> None:
        self.y = 500
        self.vy = 0
        self.on_ground = True
        self.jumps_left = 1
        self.extra_jumps = 1
    
    def update(self) -> None:
        self.motion()

        for b in self.bullets:
            b.update()


    def display(self) -> None:
        pygame.draw.circle(self.screen, self.color, (self.x, self.y - self.radius), self.radius)

        for b in self.bullets:
            b.display() 


class Bullet:
    def __init__(self, screen: pygame.Surface, x: float, y: float) -> None:
        self.screen = screen
        self.radius = 5
        self.color = "#FFD54A"

        self.x = x
        self.y = y
        self.vx = 14.0

    def update(self) -> None:
        self.x += self.vx

    def off_screen(self) -> bool:
        return self.x - self.radius > 600
    
    def display(self) -> None:
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


class Ground:
    
    def __init__(self, screen: pygame.Surface, x:int) -> None:
        self.screen = screen
        self.x = x
        self.vx = -8
        self.width = random.uniform(180,400)

    def reset(self, x) -> None:
        self.x = x
        self.width = random.uniform(180,400)
    
    def update(self) -> None:
        self.x += self.vx
        if self.x + self.width < 0:
            self.width = random.uniform(180,400)
            self.x = 800 + self.width

    def display(self) -> None:
        pygame.draw.rect(self.screen, "#FF0000", (self.x, 500, self.width, 50))

class Obstacle:
    
    def __init__(self, screen: pygame.Surface, grounds, x:float) -> None:
        self.screen = screen
        self.grounds = grounds
        self.color = "#0000FF"
        self.width = 40
        self.vx = -8
        self.x = x
        self.height = random.randrange(30, 120)

        self.health = 3

        if random.random() < 0.3:
            ground = random.choice(self.grounds)
            self.x = random.uniform(ground.x, ground.x + ground.width - self.width)
            self.y = 500 - self.height
        else:
            self.y = random.randrange(0, 450 - self.height)
    
    def hit(self) -> None:
        self.health -= 1
    
    def removed(self) -> bool:
        return self.health <= 0

    def update(self) -> None:
        self.x += self.vx

    def off_screen(self) -> bool:
        return self.x + self.width <= 0

    def display(self) -> None:
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

class HealthBar:

    def __init__(self, screen: pygame.Surface, ball) -> None:
        self.screen = screen
        self.color = "#F0EEEE"
        self.ball = ball
        self.square_size = 20
        self.square_spacing = 10
        self.y = 20

    def update(self) -> None:
        ...

    def display(self) -> None:
        for i in range(10):
            self.x = 30 + i * (self.square_size + self.square_spacing)
            if i < self.ball.health:
                self.color = "#F0EEEE"
            else:
                self.color = "#444444"
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, 20, 20))

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()

    title_font = pygame.font.SysFont('arial', 72, bold=True)
    subtitle_font = pygame.font.SysFont('arial', 28)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    score = 0
    score_font = pygame.font.SysFont('arial', 28, bold=True)

    g_one = Ground(screen, 0)
    g_two = Ground(screen, 500)
    g_three = Ground(screen, 900)
    grounds = [g_one, g_two, g_three]
    ball = Character(screen, 300, grounds)
    obstacles = [Obstacle(screen, grounds, random.randrange(300, 901)) for i in range(0,5)]
    health_bar = HealthBar(screen, ball)

    state = "start"

    while True:
        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.K_UP and state == "start":
                    score = 0
                    ball.reset()
                    g_one.reset(0)
                    g_two.reset(500)
                    g_three.reset(900)
                    state = "playing"
                    g_one.update()
                    g_one.display()
                    g_two.update()
                    g_two.display()
                    g_three.update()
                    g_three.display()
                    ball.update()
                    ball.display()
                    # health_bar.update()
                    # health_bar.display()
                if event.key == pygame.K_UP and state == "game over":
                    state = "start"

        
        if state == "start":
            screen.fill("#0000FF")
            
            title_writing = title_font.render("START GAME", True, "#FFFFFF")
            title_outline = title_writing.get_rect(center = (450, 300))

            subtitle1_writing = subtitle_font.render("Press Up to Start", True, "#FFFFFF")
            subtitle1_outline = subtitle1_writing.get_rect(center=(450, 375))

            subtitle2_writing = subtitle_font.render("Press Space to Shoot", True, "#FFFFFF")
            subtitle2_outline = subtitle2_writing.get_rect(center=(450, 425))

            screen.blit(title_writing, title_outline)
            screen.blit(subtitle1_writing, subtitle1_outline)
            screen.blit(subtitle2_writing, subtitle2_outline)

        if state == "playing":
            screen.fill("#000000")
            for i in grounds:
                i.update()
                i.display()
            for g in grounds:
                        if g.x + g.width <= 20:

                            furthest = grounds[0]
                            for platform in grounds:
                                if platform.x + platform.width > furthest.x + furthest.width:
                                    furthest = platform
                            
                            g.width = random.uniform(150, 400)
                            g.x = furthest.x + furthest.width + random.uniform(120, 340)
            ball.update()
            ball.display()
            health_bar.update()
            health_bar.display()
            for o in obstacles:
                o.update()
                o.display()
                if o.off_screen():
                    farthest = obstacles[0]
                    for obs in obstacles:
                        if obs.x > farthest.x:
                            farthest = obs
                    o.x = farthest.x + farthest.width + random.randint(50,250)
                    o.height = random.randint(30,120)
                    
                    if random.random() < 0.3:
                        ground = random.choice(grounds)
                        o.y = 500 - o.height
                    else:
                        o.y = random.randrange(0, 450 - o.height)
            
            bullets_to_remove = []
            obstacles_to_remove = []

            for b in ball.bullets:
                for o in obstacles:
                    bullet_right = b.x + b.radius
                    bullet_top = b.y - b.radius
                    bullet_bottom = b.y + b.radius

                    if (bullet_right >= o.x and
                        bullet_top <= o.y + o.height and bullet_bottom >= o.y):
                        o.hit()
                        bullets_to_remove.append(b)

                        if o.removed():
                            score += 1
                            o.health = 3

                            farthest = obstacles[0]
                            for obs in obstacles:
                                if obs.x > farthest.x:
                                    farthest = obs
                            o.x = farthest.x + farthest.width + random.randint(50,250)
                            o.height = random.randint(30,120)
                    
                            if random.random() < 0.3:
                                ground = random.choice(grounds)
                                o.y = 500 - o.height
                            else:
                                o.y = random.randrange(0, 450 - o.height)

                        
            
            for b in bullets_to_remove:
                if b in ball.bullets:
                    ball.bullets.remove(b)
            
            for o in obstacles_to_remove:
                if o in obstacles:
                    obstacles.remove(o)

            score_text = score_font.render(f"SCORE: {score}", True, "#FFFFFF")
            box = score_text.get_rect(topright=(880, 20))

            pygame.draw.rect(screen, "#000000", box)
            # pygame.draw.rect(screen, "#FFFFFF", box, 3)
            screen.blit(score_text, box)
            
            if ball.y - ball.radius >= screen.get_height():
                state = "game over"
        if state == "game over":
            screen.fill("#7A2525") #figure out how to ease it

            ending_writing = title_font.render("GAME OVER", True, "#FFFFFF")
            ending_outline = ending_writing.get_rect(center=(450, 325))
            screen.blit(ending_writing, ending_outline)

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
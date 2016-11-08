import pygame as pg
from random import uniform
from math import cos, sin, pi, degrees, radians, sqrt

# Constants
DISPLAY = WIDTH, HEIGHT = (320, 240)
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.lifetime = 0

    def update(self, screen):
        dx = int(self.x - cos(self.angle) * 10)
        dy = int(self.y - sin(self.angle) * 10)
        pg.draw.line(screen, RED, [int(self.x), int(self.y)],
                     [dx, dy])
        self.x = dx
        self.y = dy
        self.lifetime += 1


class Player:
    def __init__(self, x, y, direction, screen, speed=10, r_speed=5):
        self.x = int(x)
        self.y = int(y)
        self.direction = direction  # in radians
        self.screen = screen
        self.speed = speed
        self.r_speed = r_speed

    def draw(self):
        pg.draw.circle(self.screen, WHITE, [int(self.x), int(self.y)], 6)
        lx = int(self.x - cos(self.direction) * 15)
        ly = int(self.y - sin(self.direction) * 15)
        pg.draw.line(self.screen, WHITE, [int(self.x), int(self.y)],
                     [lx, ly])

    def move(self, delta):
        dx = (self.speed * cos(self.direction)) * delta
        dy = (self.speed * sin(self.direction)) * delta
        self.x += dx
        self.y += dy

    def rotate(self, angle):
        self.direction = (self.direction + angle + 2 * pi) % (2 * pi)

    def update(self, keys, dt):
        # move
        if keys[pg.K_w]:
            self.move(-self.speed * dt)
        if keys[pg.K_s]:
            self.move(self.speed * dt)

        # rotate
        if keys[pg.K_a]:
            self.rotate(-self.r_speed * dt)
        if keys[pg.K_d]:
            self.rotate(self.r_speed * dt)

    def __repr__(self):
        return 'Player @ {:.2f}, {:.2f}, facing {:.2f}'. \
            format(self.x, self.y, degrees(self.direction))


def main():
    pg.init()
    screen = pg.display.set_mode(DISPLAY)
    player = Player(*[n / 2 for n in DISPLAY], pi / 2.0, screen)
    clock = pg.time.Clock()
    bullets = pg.sprite.Group()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_q:
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                bullet = Bullet(player.x, player.y, player.direction)
                bullets.add(bullet)

        # time delta & key press tuples
        dt = clock.tick(30) / 1000
        keys = pg.key.get_pressed()

        # clear
        screen.fill(BLACK)

        # draw/update player
        player.update(keys, dt)
        player.draw()
        for b in bullets:
            b.update(screen)
            if b.lifetime > 10:
                b.kill()

        # update display at 30fps
        pg.display.flip()
        clock.tick(30)

    pg.quit()


if __name__ == '__main__':
    main()

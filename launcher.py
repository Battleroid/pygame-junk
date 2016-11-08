import pygame as pg
from math import pi, cos, sin, atan2, degrees

DISPLAY = WIDTH, HEIGHT = 320, 240
HALF_W = WIDTH / 2
HALF_H = HEIGHT / 2
RED = (255, 0, 0)
WHITE = (255, 255, 255)


class Launcher:
    def __init__(self, x, y, angle=45):
        self.x = x
        self.y = y
        self.angle = pi * angle / 180.0

    def update(self, x, y):
        mx = x - self.x
        my = y - self.y
        rads = atan2(-my, mx)
        rads %= 2 * pi
        self.angle = rads

    def draw(self, screen, length=20):
        # base
        pg.draw.circle(screen, WHITE, (self.x, self.y), 10)

        # draw line for direction
        dx = int(self.x + cos(self.angle) * length)
        dy = int(self.y - sin(self.angle) * length)
        pg.draw.line(screen, WHITE, [int(self.x), int(self.y)], [dx, dy])


class Bullet:

    GRAVITY = 9.81

    def __init__(self, x, y, angle, vel=50):
        self.x = x
        self.y = y
        self.xv = vel * cos(angle)
        self.yv = vel * sin(angle)

    def update(self, dt):
        dt *= 5
        self.x = self.x + dt * self.xv
        y0 = self.yv - Bullet.GRAVITY * dt
        self.y = self.y - dt * (self.yv + y0) / 2.0
        self.yv = y0

    def draw(self, screen):
        pg.draw.circle(screen, RED, (int(self.x), int(self.y)), 2)


def loop():
    BLACK = (0, 0, 0)
    LIMIT = HEIGHT - 32

    pg.init()
    screen = pg.display.set_mode(DISPLAY)
    clock = pg.time.Clock()

    launcher = Launcher(32, HEIGHT - 32)

    fired = False
    bullet = None
    while True:
        clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_q:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                fired = True
                bullet = Bullet(launcher.x, launcher.y, launcher.angle)

        dt = clock.tick(30) / 1000.0

        screen.fill(BLACK)

        launcher.update(*pg.mouse.get_pos())
        launcher.draw(screen)

        if fired:
            bullet.update(dt)
            bullet.draw(screen)

            # check if it went past our 'floor'
            if bullet.y > LIMIT:
                bullet = None
                fired = False

        pg.display.flip()


if __name__ == '__main__':
    loop()

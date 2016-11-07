import pygame as pg
from pygame import Rect, Surface
from pygame.sprite import Group, Sprite

DISPLAY = WIDTH, HEIGHT = 320, 240
HALF_W = int(WIDTH / 2)
HALF_H = int(HEIGHT / 2)
RED = (255, 0, 0)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)


class Block(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(GREY)
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass


class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.xv = 0
        self.yv = 0
        self.grounded = False
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(RED)
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, blocks):
        if up:
            if self.grounded:
                self.yv -= 13
        if down:
            pass
        if left:
            self.xv = -8
        if right:
            self.xv = 8
        if not self.grounded:
            self.yv += 1.5
            if self.yv > 110:
                self.yv = 110
        if not(left or right):
            self.xv = 0

        # increment in direction
        self.rect.left += self.xv
        self.collide(self.xv, 0, blocks)
        self.rect.top += self.yv
        self.grounded = False
        self.collide(0, self.yv, blocks)

    def collide(self, xv, yv, blocks):
        for b in blocks:
            if pg.sprite.collide_rect(self, b):
                if xv > 0:
                    self.rect.right = b.rect.left
                if xv < 0:
                    self.rect.left = b.rect.right
                if yv > 0:
                    self.rect.bottom = b.rect.top
                    self.grounded = True
                    self.yv = 0
                if yv < 0:
                    self.rect.top = b.rect.bottom
                    self.yv = 0  # bounce back immediately if blocked


class Camera:
    def __init__(self, cam_type, width, height):
        self.cam_type = cam_type
        self.width = width
        self.height = height
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.cam_type(self.state, target.rect)

    @staticmethod
    def simple(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        return Rect(-l + HALF_W, -t + HALF_H, w, h)

    @staticmethod
    def complex(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l + HALF_W, -t + HALF_H, w, h

        l = min(0, l)
        l = max(-(camera.width - WIDTH), l)
        t = max(-(camera.height - HEIGHT), t)
        t = min(0, t)

        return Rect(l, t, w, h)


def loop():
    # init
    pg.init()
    screen = pg.display.set_mode(DISPLAY)
    clock = pg.time.Clock()

    # level generation
    x = y = 0
    level = [
            "ppppppppppppppppp",
            "p               p",
            "p        ppp    p",
            "p               p",
            "p  pppp         p",
            "p      p  ppp   p",
            "p               p",
            "p   ppppp       p",
            "p               p",
            "ppppppppppppppppp"
            ]

    # entities and blocks
    entities = Group()
    blocks = []
    for row in level:
        for col in row:
            if col == 'p':
                block = Block(x, y)
                blocks.append(block)
                entities.add(block)
            x += 32
        y += 32
        x = 0

    # set camera
    total_width = len(level[0]) * 32
    total_height = len(level) * 32
    camera = Camera(Camera.complex, total_width, total_height)

    # set bg
    bg = Surface((32, 32))
    bg.convert()
    bg.fill(BLACK)

    # add player
    player = Player(64, 64)
    entities.add(player)

    up = down = left = right = False
    while True:
        clock.tick(30)

        # process events/keys
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
            if e.type == pg.KEYDOWN and e.key == pg.K_q:
                pg.quit()

            # movement
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_a:
                    left = True
                if e.key == pg.K_d:
                    right = True
                if e.key == pg.K_w:
                    up = True
                if e.key == pg.K_s:
                    down = True

            # release
            if e.type == pg.KEYUP:
                if e.key == pg.K_a:
                    left = False
                if e.key == pg.K_d:
                    right = False
                if e.key == pg.K_w:
                    up = False
                if e.key == pg.K_s:
                    down = False

        # draw
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))
        camera.update(player)
        player.update(up, down, left, right, blocks)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pg.display.update()


if __name__ == '__main__':
    loop()

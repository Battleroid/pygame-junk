import pygame as pg


DISPLAY = W, H = (320, 240)
WH = int(W / 2)
HH = int(H / 2)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Block(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface([32, 32])
        self.image.convert()
        self.image.fill(GREY)
        self.rect = pg.Rect(x, y, 32, 32)

    def update(self):
        pass


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.xvel = 0
        self.yvel = 0
        self.image = pg.Surface([32, 32])
        self.image.fill(RED)
        self.image.convert()
        self.rect = pg.Rect(x, y, 32, 32)

    def update(self, u, d, l, r, blocks):
        if u:
            self.yvel = -32
        if d:
            self.yvel = 32
        if l:
            self.xvel = -32
        if r:
            self.xvel = 32

        self.rect.left += self.xvel
        self.collide(self.xvel, 0, blocks)
        self.rect.top += self.yvel
        self.collide(0, self.yvel, blocks)

        self.xvel = 0
        self.yvel = 0

    def collide(self, xvel, yvel, blocks):
        for b in blocks:
            if pg.sprite.collide_rect(self, b):
                if xvel > 0:
                    self.rect.right = b.rect.left
                if xvel < 0:
                    self.rect.left = b.rect.right
                if yvel > 0:
                    self.rect.bottom = b.rect.top
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = b.rect.bottom


class Camera:
    def __init__(self, cam_type, width, height):
        self.cam_type = cam_type
        self.state = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.cam_type(self.state, target.rect)


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pg.Rect(-l + WH, -t + HH, w, h)


def loop():
    # start
    pg.init()
    screen = pg.display.set_mode(DISPLAY)
    clock = pg.time.Clock()

    # build sample level
    sample_level = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
            ]

    # add entity blocks
    entities = pg.sprite.Group()
    blocks = []
    x = y = 0
    for row in sample_level:
        for col in row:
            if col == 1:
                blk = Block(x, y)
                blocks.append(blk)
                entities.add(blk)
            x += 32
        y += 32
        x = 0

    # set camera
    total_width = len(sample_level[0]) * 32
    total_height = len(sample_level) * 32
    camera = Camera(simple_camera, total_width, total_height)
    player = Player(32, 32)
    entities.add(player)
    bg = pg.Surface([32, 32])
    bg.convert()
    bg.fill(BLACK)

    up = down = left = right = False
    while True:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_q:
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    left = True
                if event.key == pg.K_d:
                    right = True
                if event.key == pg.K_w:
                    up = True
                if event.key == pg.K_s:
                    down = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    left = False
                if event.key == pg.K_d:
                    right = False
                if event.key == pg.K_w:
                    up = False
                if event.key == pg.K_s:
                    down = False

        # draw
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        player.update(up, down, left, right, blocks)
        camera.update(player)

        # update display
        pg.display.flip()


if __name__ == '__main__':
    loop()

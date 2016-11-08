from random import uniform


def midpoint(points, n=5):
    return _midpoint(points, n)


def _midpoint(points, n, rough=50, scale=0.75):
    if n == 0:
        return points

    new_points = [points[0]]

    for i in range(len(points) - 1):
        avg_x = (points[i][0] + points[i + 1][0]) / 2.0
        avg_y = (points[i][1] + points[i + 1][1]) / 2.0
        mid = avg_x, avg_y + uniform(-rough, rough)

        new_points.append(mid)
        new_points.append(points[i + 1])

    return _midpoint(new_points, n - 1, rough * (2 ** -scale), scale)


if __name__ == '__main__':
    import pygame as pg

    DISPLAY = WIDTH, HEIGHT = 320, 240
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    pg.init()
    screen = pg.display.set_mode(DISPLAY)
    clock = pg.time.Clock()

    n = 5

    def demo(n):
        points = [[0, HEIGHT / 2], [WIDTH, HEIGHT / 2]]
        points = midpoint(points, n=n)
        points.append([WIDTH, HEIGHT])
        points.append([0, HEIGHT])
        return points

    screen.fill(BLACK)
    terrain = pg.draw.polygon(screen, WHITE, demo(n), 0)
    font = pg.font.SysFont('monospace', 12)
    label = font.render(str(n), 1, WHITE)
    screen.blit(label, (10, 10))

    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_q:
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                screen.fill(BLACK)
                label = font.render(str(n), 1, WHITE)
                screen.blit(label, (10, 10))
                terrain = pg.draw.polygon(screen, WHITE, demo(n), 0)
            if event.type == pg.KEYDOWN and event.key == pg.K_n:
                n += 1

        clock.tick(30)

        pg.display.update()

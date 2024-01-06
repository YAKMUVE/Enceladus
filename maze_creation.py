import pygame
from maze import Maze

white = 255, 255, 255

screen = pygame.display.set_mode((700, 650))
background_image = pygame.image.load('background_4.jpg')
background_image = pygame.transform.scale(background_image, (700, 650))

MAZE_SIZE = (10, 20)
CELL_SIZE = 20

m = Maze(MAZE_SIZE)
sol = []

bx, by = (80, 80)


def maze_drawer():
    if not (x - 1, y, x, y) in m.doors and not (x + y == 0):
        pygame.draw.line(screen, white, (bx + x * CELL_SIZE, by + y * CELL_SIZE),
                         (bx + x * CELL_SIZE, by + (y + 1) * CELL_SIZE))
    else:
        if (x - 1, y) in sol and (x, y) in sol:
            pygame.draw.line(screen, (0, 255, 0),
                             (bx + x * CELL_SIZE - CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2),
                             (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2))

    if not (x, y, x + 1, y) in m.doors:
        pygame.draw.line(screen, white, (bx + (x + 1) * CELL_SIZE, by + y * CELL_SIZE),
                         (bx + (x + 1) * CELL_SIZE, by + (y + 1) * CELL_SIZE))
    else:
        if (x, y) in sol and (x + 1, y) in sol:
            pygame.draw.line(screen, (0, 255, 0),
                             (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2),
                             (bx + x * CELL_SIZE + 3 * (CELL_SIZE // 2), by + y * CELL_SIZE + CELL_SIZE // 2))

    if not (x, y - 1, x, y) in m.doors:
        pygame.draw.line(screen, white, (bx + x * CELL_SIZE, by + y * CELL_SIZE),
                         (bx + (x + 1) * CELL_SIZE, by + y * CELL_SIZE))
    else:
        if (x, y - 1) in sol and (x, y) in sol:
            pygame.draw.line(screen, (0, 255, 0),
                             (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE - CELL_SIZE // 2),
                             (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2))

    if not (x, y, x, y + 1) in m.doors and not (x + y == MAZE_SIZE[0] + MAZE_SIZE[1] - 2):
        pygame.draw.line(screen, white, (bx + x * CELL_SIZE, by + (y + 1) * CELL_SIZE),
                         (bx + (x + 1) * CELL_SIZE, by + (y + 1) * CELL_SIZE))
    else:
        if (x, y) in sol and (x, y + 1) in sol:
            pygame.draw.line(screen, (0, 255, 0),
                             (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2),
                             (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + 3 * (CELL_SIZE // 2)))


running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for x in range(MAZE_SIZE[0]):
        for y in range(MAZE_SIZE[1]):
            maze_drawer()

    pygame.display.update()

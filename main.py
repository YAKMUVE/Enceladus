import pygame
from pygame.locals import KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_


# объявление const
DISPLAY = WIN_WIDTH, WIN_HEIGHT = 800, 600
FPS = 60
MOVE_SPEED = 7

# инициализация
pygame.init()

# подготовка переменных
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption('Enceladus')
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()


class Object(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, path: str, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height

        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def rotate(self, degrees: int):
        self.image = pygame.transform.rotate(self.image, degrees)


class Player(Object):
    def __init__(self, x: int, y: int):
        super().__init__(64, 64, 'Sprites\\char_sprite_1.png', x, y)
        self.health = 3
        self.directions = {
            'NORTH': -MOVE_SPEED,
            'SOUTH': MOVE_SPEED,
            'EAST': MOVE_SPEED,
            'WEST': -MOVE_SPEED
        }

    def movement(self, direction: str):
        if direction == 'NORTH' or direction == 'SOUTH':
            self.rect.y += self.directions[direction]
        elif direction == 'EAST' or direction == 'WEST':
            self.rect.x += self.directions[direction]


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


if __name__ == '__main__':
    while pygame.quit() not in pygame.event.wait().type:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
        # обновление и вывод
        sprites.update()
        pygame.display.update()

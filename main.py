import pygame
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN

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
        super().__init__(64, 64, 'Enceladus\\Sprites\\char_sprite_1.png', x, y)
        self.health = 3

    def update(self):
        keystate = pygame.key.get_pressed()
        self.movement(keystate)
        self.border_control()

    def movement(self, keystate):
        if keystate[K_UP]:
            self.rect.y -= MOVE_SPEED
        if keystate[K_DOWN]:
            self.rect.y += MOVE_SPEED
        if keystate[K_LEFT]:
            self.rect.x -= MOVE_SPEED
        if keystate[K_RIGHT]:
            self.rect.x += MOVE_SPEED

    def border_control(self):
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


if __name__ == '__main__':
    player = Player(50, 50)
    sprites.add(player)
    running = True
    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        sprites.update()

        # Рендеринг
        sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

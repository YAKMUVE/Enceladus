import pygame
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN

# const
DISPLAY = WIN_WIDTH, WIN_HEIGHT = 800, 600
FPS = 60
MOVE_SPEED = 7

# const цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# инициализация
pygame.init()

# подготовка
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption('Enceladus')
clock = pygame.time.Clock()
entity = pygame.sprite.Group()
immovable = pygame.sprite.Group()


class Object(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, path: str, x: int, y: int):
        """
        :width: длина объекта
        :height: высота объекта
        :path: путь до спрайта объекта
        :x: координата объекта по оски x
        :y: координата объекта по оски y
        """
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height

        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(Object):
    def __init__(self, x: int, y: int):
        """
        :x: координата объекта по оски x
        :y: координата объекта по оски y
        """
        super().__init__(64, 64, 'Sprites/general/char_sprite_1.png', x, y)
        self.health = 3

        # трекер движения игрока
        self.upward = False
        self.downward = False
        self.leftward = False
        self.rightward = False

    def update(self):
        self.movement()
        self.conflict()
        self.border_control()

    def definition(self, key: int):
        """
        definition отслеживает передвижения игрока

        :key: ключ (id) нажатой кнопки
        """
        if key == K_UP and not self.tracking(): self.upward = True
        if key == K_DOWN and not self.tracking(): self.downward = True
        if key == K_LEFT and not self.tracking(): self.leftward = True
        if key == K_RIGHT and not self.tracking(): self.rightward = True

    def tracking(self) -> bool:
        """
        :return: направляется ли уже куда-то игрок
        """
        valid = self.upward or self.downward or self.leftward or self.rightward
        return valid

    def movement(self):
        """
        movement передвигает игрока
        """
        if self.upward: self.rect.y -= MOVE_SPEED
        if self.downward: self.rect.y += MOVE_SPEED
        if self.leftward: self.rect.x -= MOVE_SPEED
        if self.rightward: self.rect.x += MOVE_SPEED

    def conflict(self):
        """
        confict останавливает игрока, в случае столкновения с другим объектом
        """
        hit = pygame.sprite.spritecollide(player, immovable, False)

        for collision in hit:
            if self.upward: self.upward = False
            if self.downward: self.downward = False
            if self.leftward: self.leftward = False
            if self.rightward: self.rightward = False

    def border_control(self):
        """
        border_control останавливает игрока, в случае выхода за границу
        """
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
            self.rightward = False

        if self.rect.left < 0:
            self.rect.left = 0
            self.leftward = False

        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT
            self.downward = False

        if self.rect.top < 0:
            self.rect.top = 0
            self.upward = False


# class Camera(object):
#     def __init__(self, camera_func, width, height):
#         self.camera_func = camera_func
#         self.state = pygame.Rect(0, 0, width, height)
#
#     def apply(self, target):
#         return target.rect.move(self.state.topleft)
#
#     def update(self, target):
#         self.state = self.camera_func(self.state, target.rect)


def render():
    screen.fill(BLACK)

    # отрисовка
    entity.update()
    immovable.update()

    # Рендеринг
    entity.draw(screen)
    immovable.draw(screen)
    pygame.display.flip()


if __name__ == '__main__':
    player = Player(50, 50)
    entity.add(player)
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                player.definition(event.key)
            if event.type == pygame.QUIT:
                running = False

        render()

    pygame.quit()

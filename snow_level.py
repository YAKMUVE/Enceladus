import pygame
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN
import random

# const
DISPLAY = WIN_WIDTH, WIN_HEIGHT = 600, 650
FPS = 60
MOVE_SPEED = 8

# const цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# # инициализация
# pygame.init()
#
# # подготовка
# screen = pygame.display.set_mode(DISPLAY)
# pygame.display.set_caption('Enceladus')
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
        super().__init__(64, 64, 'char_sprite_1.png', x, y)
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

player = Player(50, 50)


class Level2:
    def __init__(self):
        pygame.init()
        size = (650, 650)
        self.screen_width = 600
        self.screen_height = 650
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Level 2')
        self.color = '#ffffff'
        self.background_image = pygame.image.load('level_background.png')
        self.background_image = pygame.transform.scale(self.background_image, size)
        self.landed = 0

        self.screen.blit(self.background_image, (0, 0))
        pygame.display.flip()

        self.snowflakes = []
        self.snow_per_pixel = 250
        self.level_height = 0

        self.clock = pygame.time.Clock()

    def add_drop(self):
        self.snowflakes.append([random.randint(0, self.screen_width), 0])

    # рисование снежинок
    def snowflake_painter(self):
        for i in self.snowflakes:
            pygame.draw.line(self.screen, self.color, (i[0], i[1]), (i[0], i[1] + 2), 3)

    # подъем уровня
    def update_drops(self):
        for i in self.snowflakes:
            i[1] += 5
            if i[1] >= self.screen_height:
                self.snowflakes.remove(i)
                self.landed += 10
                if self.landed % self.snow_per_pixel == 0:
                    self.level_height += 3

    # рисование уровня снега
    def level_painter(self):
        pygame.draw.rect(self.screen, self.color,
                         (0, self.screen_height - self.level_height, self.screen_width, self.level_height))

    def render(self):

        # отрисовка
        entity.update()
        immovable.update()

        # Рендеринг
        entity.draw(self.screen)
        immovable.draw(self.screen)
        pygame.display.flip()

    # проверка соприкосновения со снегом
    def position_cheker(self, char):
        snow_pos = self.screen_height - self.level_height
        char_pos = char.rect.bottom
        if snow_pos <= char_pos:
            return False
        return True

    def run(self):
        player = Player(50, 50)
        entity.add(player)
        running = True
        while running:
            clock.tick(FPS)
            if not self.position_cheker(player):
                running = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    player.definition(event.key)
                if event.type == pygame.QUIT:
                    running = False
            self.add_drop()
            self.update_drops()
            self.screen.blit(self.background_image, (0, 0))
            self.snowflake_painter()
            self.level_painter()
            self.clock.tick(35)
            self.render()

        pygame.quit()


if __name__ == "__main__":
    app = Level2()
    app.run()

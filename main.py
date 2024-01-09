import pygame
from pygame import Surface
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, Color
import sqlite3 as sq
import random

# const
DISPLAY = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
FPS = 35
MOVE_SPEED = 7

# const paths
DIR_GENERAL = 'Sprites/general'
DIR_BACKGROUNDS = 'Sprites/backgrounds'
DIR_LEVEL_1 = 'Sprites/level_1'
DIR_LEVEL_2 = 'Sprites/level_2'
DIR_LEVEL_3 = 'Sprites/level_3'
DIR_LEVEL_4 = 'Sprites/level_4'

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
players = pygame.sprite.Group()
current_display = pygame.sprite.Group()



def database_maker():
    con = sq.connect('progress.db')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS 'achievements'(
        'level'   TEXT,
        'sum' INTEGER,
        'weapon'  TEXT,
        'extra'   TEXT
    );
    """)
    con.commit()
    r = cur.execute("""SELECT * FROM 'achievements'""").fetchall()
    if not r:
        cur.execute("""INSERT INTO 'achievements'(level) VALUES('0')""")
        con.commit()
    con.close()


def database_changer(column, value):
    con = sq.connect('progress.db')
    cur = con.cursor()
    cur.execute(f"UPDATE 'achievements' SET {column}=?", (value, ))
    con.commit()
    con.close()


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

    def coord_returner(self):
        return (self.rect.x, self.rect.y)


class Entity(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, path: str, x: int, y: int):
        """
        :width: длина сущности
        :height: высота сущности
        :path: путь до спрайта сущности
        :x: координата объекта по оски x
        :y: координата объекта по оски y
        """
        pygame.sprite.Sprite.__init__(self)
        self.purposes = None
        self.speed = None

        self.width = width
        self.height = height

        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # трекер движения
        self.upward = False
        self.downward = False
        self.leftward = False
        self.rightward = False

    def init_trajectory(self, speed: int, purposes: list):
        self.speed = speed
        self.purposes = purposes

    def update(self):
        self.tracking()
        self.movement()

    def tracking(self):
        pass

    def movement(self):
        """
        movement передвигает сущность
        """
        if self.upward: self.rect.y -= self.speed
        if self.downward: self.rect.y += self.speed
        if self.leftward: self.rect.x -= self.speed
        if self.rightward: self.rect.x += self.speed


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
        pass

    def border_control(self):
        """
        border_control останавливает игрока, в случае выхода за границу
        """
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.rightward = False

        if self.rect.left < 0:
            self.rect.left = 0
            self.leftward = False

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
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


class Levels(pygame.sprite.Sprite):
    def __init__(self, background_path: str, markup: str, designations: dict):
        pygame.sprite.Sprite.__init__(self)
        self.background_path = background_path
        self.markup = markup
        self.designations = designations

        self.entities = pygame.sprite.Group()
        self.immovable = pygame.sprite.Group()

        self.entities.add(Object(64, 64, f'{DIR_GENERAL}/char_sprite_1.png', 200, 200))
        self.immovable.add(Object(44, 44, f'{DIR_GENERAL}/block.png', 40, 100))
        # k1, k2 =10, 10
        # for i in range(10):
        #     self.immovable.add(Object(44, 44, f'{DIR_GENERAL}/block.png', k1, k2))
        #     k1 += 44

        self.background_image = False
        self.background_rect = None

    # def generation(self):
    #     x, y = 0, 0
    #     for line in self.markup:
    #         for elem in line:
    #             decoding = self.designations.get(elem, False)
    #             if isinstance(decoding, Entity):
    #                 self.entities.add(decoding)
    #             elif isinstance(decoding, Object):
    #                 self.immovable.add(decoding)
    #
    #             x += decoding.width
    #             if elem == line[-1]:
    #                 y += decoding.height
    #                 x = 0


    def load_background(self):
        self.background_image = pygame.image.load(self.background_path)
        self.background_image = pygame.transform.scale(self.background_image, DISPLAY)

        self.background_rect = self.background_image.get_rect()
        self.background_rect.x = 0
        self.background_rect.y = 0




class Level1(Levels):
    def __init__(self):
        Levels.__init__(self, f'{DIR_BACKGROUNDS}/lvl1_background.png', '', {})
        self.color = '#4db2ff'
        self.landed = 0

        self.snowflakes = []
        self.snow_per_pixel = 250
        self.level_height = 0

    def update(self):
    #     self.add_drop()
    #     self.update_drops()
    #
    #     self.snowflake_painter()
    #     self.level_painter()
    #
        if self.background_image:
            screen.blit(self.background_image, (0, 0))

    def add_drop(self):
        self.snowflakes.append([random.randint(0, SCREEN_WIDTH), 0])

    # рисование снежинок
    def snowflake_painter(self):
        for i in self.snowflakes:
            pygame.draw.line(screen, self.color, (i[0], i[1]), (i[0], i[1] + 7), 3)


    # подъем уровня
    def update_drops(self):
        for i in self.snowflakes:
            i[1] += 5
            if i[1] >= SCREEN_HEIGHT:
                self.snowflakes.remove(i)
                self.landed += 10
                if self.landed % self.snow_per_pixel == 0:
                    self.level_height += 3

    # рисование уровня снега
    def level_painter(self):
        pygame.draw.rect(screen, self.color,
                         (0, SCREEN_HEIGHT - self.level_height, SCREEN_WIDTH, self.level_height))

    def position_cheker(self, char):
        snow_pos = SCREEN_HEIGHT - self.level_height
        char_pos = char.rect.bottom
        if snow_pos <= char_pos:
            return False
        return True

def render():

    # отрисовка
    players.update()
    # current_level.update()

    # Рендеринг
    players.draw(screen)
    current_display.draw(screen)
    pygame.display.flip()


if __name__ == '__main__':
    database_maker()
    player = Player(50, 50)
    current_level = Level1()
    # camera = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    players.add(player)

    level = int(input())
    flag = False

    running = True
    while running:
        current_level.update()
        clock.tick(FPS)

        if not(current_level.position_cheker(player)):
            running = False

        if level == 1 and not flag:
            current_level.load_background()

            # current_display.add(current_level.entities)
            current_display.add(current_level.immovable)

            flag = True

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                player.definition(event.key)
            if event.type == pygame.QUIT:
                running = False
        current_level.add_drop()
        current_level.update_drops()
        current_level.snowflake_painter()
        current_level.level_painter()
        clock.tick(40)
        render()

    pygame.quit()

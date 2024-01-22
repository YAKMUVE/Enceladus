from maze import Maze
from pause import *
from level4 import *
import time

# const
DISPLAY = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
FPS = 60
MOVE_SPEED = 7
MAZE_SIZE = (16, 22)
CELL_SIZE = 35

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
screen = pygame.display.set_mode(DISPLAY, pygame.NOFRAME)
clock = pygame.time.Clock()
players = pygame.sprite.Group()
current_display = pygame.sprite.Group()

win_sound = pygame.mixer.Sound('Sounds/win_sound.mp3')
lose_sound = pygame.mixer.Sound('Sounds/gameover_sound.mp3')


class Object(pygame.sprite.Sprite):  # основной класс объекта
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


class Player(Object):  # класс игрока
    def __init__(self, x: int, y: int, skin):
        # :x: координата объекта по оси x
        # :y: координата объекта по оси y
        super().__init__(25, 25, skin, x, y)
        self.old_coord = (self.rect.x, self.rect.y)

    def update(self):  # обновление параметров игрока
        self.movement()
        self.conflict()
        self.border_control()

    def movement(self):  # движение игрока в случае нажатия на клавишу
        self.old_coord = (self.rect.x, self.rect.y)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.rect.y -= MOVE_SPEED
        if keys[pygame.K_s]: self.rect.y += MOVE_SPEED
        if keys[pygame.K_a]: self.rect.x -= MOVE_SPEED
        if keys[pygame.K_d]: self.rect.x += MOVE_SPEED

    def conflict(self):
        # confict останавливает игрока, в случае столкновения с другим объектом
        if any(self.rect.clipline(*line) for line in lines):
            self.rect.x, self.rect.y = self.old_coord

    def border_control(self):
        # border_control останавливает игрока, в случае выхода за границу
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.rect.top < 0:
            self.rect.top = 0

    def finish(self, l):
        # повышение уровня по достижении финальных координат
        if self.rect.left == 0:
            database_changer('level', int(l) + 1)
            return True
        return False


class Levels(pygame.sprite.Sprite):  # общий класс уровней
    def __init__(self, background_path: str, markup: str, designations: dict):
        pygame.sprite.Sprite.__init__(self)
        self.background_path = background_path
        self.markup = markup
        self.designations = designations

        self.immovable = pygame.sprite.Group()

        self.background_image = False
        self.background_rect = None

        self.color = WHITE
        self.landed = 0  # количество приземленных снежинок

        self.snowflakes = []  # список всех снежинок
        self.snow_per_pixel = 250  # скорость снежинок
        self.level_height = 0  # уровень снега

    def load_background(self):
        # подгрузка фона
        self.background_image = pygame.image.load(self.background_path)
        self.background_image = pygame.transform.scale(self.background_image, DISPLAY)

        self.background_rect = self.background_image.get_rect()
        self.background_rect.x = 0
        self.background_rect.y = 0

    # добавление новых снежинок
    def add_drop(self):
        self.snowflakes.append([random.randint(0, SCREEN_WIDTH), 0])

    # рисование снежинок
    def snowflake_painter(self):
        for i in self.snowflakes:
            pygame.draw.line(screen, self.color, (i[0], i[1]), (i[0], i[1] + 7), 3)

    # подъем уровня на высоту lh
    def update_drops(self, lh):
        for i in self.snowflakes:
            i[1] += 5
            if i[1] >= SCREEN_HEIGHT:
                self.snowflakes.remove(i)
                self.landed += 10
                if self.landed % self.snow_per_pixel == 0:
                    self.level_height += lh

    # рисование уровня снега
    def level_painter(self):
        pygame.draw.rect(screen, self.color,
                         (0, SCREEN_HEIGHT - self.level_height, SCREEN_WIDTH, self.level_height))

    def position_cheker(self, char):
        # проверка, больше ли уровень снега чем координаты игрока
        snow_pos = SCREEN_HEIGHT - self.level_height
        char_pos = char.rect.bottom
        if snow_pos <= char_pos:
            return False
        return True

    def update(self):  # отображение фона
        if self.background_image:
            screen.blit(self.background_image, (0, 0))


class Level1(Levels):  # класс уровня 1
    def __init__(self):
        Levels.__init__(self, f'{DIR_BACKGROUNDS}/lvl1_background.png', '', {})


class Level2(Levels):  # класс уровня 2
    def __init__(self):
        Levels.__init__(self, f'{DIR_BACKGROUNDS}/lvl2_background.png', '', {})


def render():
    # отрисовка
    players.update()

    # Рендеринг
    players.draw(screen)
    current_display.draw(screen)
    pygame.display.flip()


m = Maze(MAZE_SIZE)
sol = []

bx, by = (10, 10)


def maze_drawer1(x, y):  # отрисовка лабиринта по заданным координатам
    if not (x - 1, y, x, y) in m.doors and not (x + y == 0):
        coords = ((bx + x * CELL_SIZE, by + y * CELL_SIZE), (bx + x * CELL_SIZE, by + (y + 1) * CELL_SIZE))
        pygame.draw.line(screen, WHITE, coords[0], coords[1], 4)
        lines.append(coords)

    else:
        if (x - 1, y) in sol and (x, y) in sol:
            coords = ((bx + x * CELL_SIZE - CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2),
                      (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2))

            pygame.draw.line(screen, (0, 255, 0), coords[0], coords[1], 4)
            lines.append(coords)

    if not (x, y, x + 1, y) in m.doors:
        coords = ((bx + (x + 1) * CELL_SIZE, by + y * CELL_SIZE),
                  (bx + (x + 1) * CELL_SIZE, by + (y + 1) * CELL_SIZE))
        pygame.draw.line(screen, WHITE, coords[0], coords[1], 4)
        lines.append(coords)

    else:
        if (x, y) in sol and (x + 1, y) in sol:
            coords = ((bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2),
                      (bx + x * CELL_SIZE + 3 * (CELL_SIZE // 2), by + y * CELL_SIZE + CELL_SIZE // 2))
            pygame.draw.line(screen, (0, 255, 0), coords[0], coords[1], 4)
            lines.append(coords)

    if not (x, y - 1, x, y) in m.doors:
        coords = ((bx + x * CELL_SIZE, by + y * CELL_SIZE), (bx + (x + 1) * CELL_SIZE, by + y * CELL_SIZE))
        pygame.draw.line(screen, WHITE, coords[0], coords[1], 4)
        lines.append(coords)

    else:
        if (x, y - 1) in sol and (x, y) in sol:
            coords = ((bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE - CELL_SIZE // 2),
                      (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2))
            pygame.draw.line(screen, (0, 255, 0), coords[0], coords[1], 4)
            lines.append(coords)

    if not (x, y, x, y + 1) in m.doors and not (x + y == MAZE_SIZE[0] + MAZE_SIZE[1] - 2):
        coords = ((bx + x * CELL_SIZE, by + (y + 1) * CELL_SIZE),
                  (bx + (x + 1) * CELL_SIZE, by + (y + 1) * CELL_SIZE))
        pygame.draw.line(screen, WHITE, coords[0], coords[1], 4)
        lines.append(coords)
    else:
        if (x, y) in sol and (x, y + 1) in sol:
            coords = ((bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + CELL_SIZE // 2),
                      (bx + x * CELL_SIZE + CELL_SIZE // 2, by + y * CELL_SIZE + 3 * (CELL_SIZE // 2)))
            pygame.draw.line(screen, (0, 255, 0), coords[0], coords[1], 4)
            lines.append(coords)


def maze_drawer2():  # передача координат функции maze_drawer1
    [maze_drawer1(x, y) for x in range(MAZE_SIZE[0]) for y in range(MAZE_SIZE[1])]


def snow_level_painter(current_level, H):  # обновление уровня снега
    current_level.add_drop()
    current_level.update_drops(H)
    current_level.snowflake_painter()
    current_level.level_painter()
    clock.tick(30)


def discard(current_level):  # обнуление прогресса
    current_level.landed = 0
    current_level.snowflakes = []
    current_level.snow_per_pixel = 300
    current_level.level_height = 0


lines = []


def common_lvl_run(player):  # функция запуска основного цикла
    global lines

    # определение уровня
    current_level = Level1()
    H = 0
    l = level_determinant()
    if l == 1:
        current_level = Level1()
        H = 3
    if l == 2:
        current_level = Level2()
        H = 5

    players.add(player)

    flag = False
    running = True
    while running:
        lines = []
        current_level.update()
        clock.tick(FPS)

        # вызов экрана выигрыша по достижении игроком финальных координат
        if player.finish(l):
            time.sleep(0.5)
            win_sound.play()
            resize_screen((500, 500))
            w = win(screen, 20)
            discard(current_level)
            players.remove(player)

            with open('chosen_skin.json', 'w'):
                common_score = read_money()
            with open('money.json', 'w') as json_file:
                json.dump(common_score + 20, json_file)
            if w == 'to menu':
                return 'to menu'

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # обнуление данных и возврат размера экрана к размерам меню в случае выхода из игры
                if event.key == pygame.K_ESCAPE:
                    players.remove(player)
                    resize_screen((750, 500))
                    discard(current_level)
                    return 'to menu'

                # пауза в случае нажатия Enter
                # и изменение размера игрового экрана согласно размерам экрана паузы
                if event.key == pygame.K_RETURN:
                    pause_screen(screen)
                    resize_screen(DISPLAY)

        # вызов экрана проигрыша, если игрок соприкоснулся со снегом
        if not (current_level.position_cheker(player)):
            time.sleep(0.5)
            lose_sound.play()
            resize_screen((500, 500))
            f = main_gameover(screen)
            discard(current_level)
            if f == 'to menu':
                players.remove(player)
                return 'to menu'
            # если игрок хочет попробовать еще раз, возвращение к начальным данным и параметрам
            resize_screen(DISPLAY)
            player.rect.x, player.rect.y = 535, 750

        if not flag:
            current_level.load_background()
            current_display.add(current_level.immovable)
            flag = True

        maze_drawer2()
        snow_level_painter(current_level, H)
        render()

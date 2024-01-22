import random
from win_screen import *
from db_worker import *
from game_over_screen import *
from pause import *

pygame.init()
DISPLAY = SCREEN_WIDTH, SCREEN_HEIGHT = 700, 650
screen = pygame.display.set_mode(DISPLAY, pygame.NOFRAME)
clock = pygame.time.Clock()

background_image = pygame.image.load('Sprites/backgrounds/lvl4_background.jpg')
background_image = pygame.transform.scale(background_image, DISPLAY)
background_rect = background_image.get_rect()
all_sprites = pygame.sprite.Group()
win_sound = pygame.mixer.Sound('Sounds/win_sound.mp3')
lose_sound = pygame.mixer.Sound('Sounds/gameover_sound.mp3')


class Spaseship(pygame.sprite.Sprite):  # класс корабля
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/general/spaceship_pic.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 350

    def movement(self):  # реализация движения в случае нажатия клавиши
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and ship.rect.x != 0:
            ship.rect.x -= 5
        elif keys[pygame.K_d] and ship.rect.x < 640:
            ship.rect.x += 5


class FallingImage:  # класс астероида
    def __init__(self, x):
        #  подгузка изображения и его координат
        pic = pygame.image.load('Sprites/general/asteroid_pic.png')
        self.image = pygame.transform.scale(pic.convert_alpha(), (70, 70))
        self.x = x
        self.y = random.randint(-100, -10)

    def draw(self):  # отрисовка изображения астероида
        screen.blit(self.image, (self.x, self.y))

    def score_counter(self):
        global SCORE
        if self.y == 600:
            SCORE += 1
            with open('money.json', 'w') as json_file:
                json.dump(common_score + SCORE, json_file)

    def ast_count(self, k):
        if self.y == 600:
            k += 1
            return k
        return k


with open("money.json", "r") as json_file:  # подгрузка общего счета
    common_score = json.load(json_file)


def pos_cheker(arg, c):  # генерация новых случайных координат, если объект вышел за нижний предел экрана
    if arg.y > 700:
        arg.y = -100
        arg.x = random.choice(c)


def collision_ast():  # проверка коллизии с астероидами
    if any(ship.rect.collidepoint(ast.x, ast.y) for ast in asteroids):
        return True
    return False


SCORE = 0  # текущий счет

# объекты астероидов
ast1, ast2, ast3, ast4 = FallingImage(400), FallingImage(100), FallingImage(200), FallingImage(50)
asteroids = [ast1, ast2, ast3, ast4]

# списки координат объектов
c1 = [50, 80, 110, 150]
c2 = [200, 250, 300]
c3 = [350, 400, 450]
c4 = [500, 550]
c5 = [550, 600]

ship = Spaseship()


def run_lvl4():  # функция запуска основного цикла
    global SCORE
    run = True
    asteroid_k = 0

    while run:
        clock.tick(55)
        screen.blit(background_image, (0, 0))

        # вызов экрана выигрыша, если убитых врагов больше 20
        # и сохранение заработанного счета
        if asteroid_k > 50:
            win_sound.play()
            resize_screen((500, 500))
            w = win(screen, SCORE)
            with open('chosen_skin.json', 'w'):
                common_score = read_money()
            with open('money.json', 'w') as json_file:
                json.dump(common_score + 20, json_file)
            return w

        # обновление параметров астероидов и их подсчет
        for i in asteroids:
            i.draw()
            i.score_counter()
            asteroid_k = i.ast_count(asteroid_k)
        ast1.y += 3
        ast2.y += 6
        ast3.y += 4
        ast4.y += 5
        pos_cheker(ast1, c1)
        pos_cheker(ast2, c2)
        pos_cheker(ast3, c3)
        pos_cheker(ast4, c4)

        # проверка на коллизию астероида и игрока: если она произошла, вызов экрана проигрыша
        # и сохранение заработанного счета, обнуление данных
        if collision_ast():
            lose_sound.play()
            with open('chosen_skin.json', 'w'):
                common_score = read_money()
            with open('money.json', 'w') as json_file:
                json.dump(common_score + 20, json_file)
            with open('money.json', 'w') as json_file:
                json.dump(common_score + SCORE, json_file)
            resize_screen((500, 500))
            m = main_gameover(screen)
            ship.rect.x = 10
            ast1.y = random.randint(-100, -10)
            ast2.y = random.randint(-100, -10)
            ast3.y = random.randint(-100, -10)
            ast4.y = random.randint(-100, -10)
            SCORE = 0

            if m == 'to menu':
                return 'to menu'
            else:
                # если игрок хочет попробовать еще раз, возвращение к начальным данным и параметрам
                resize_screen((700, 650))
                ship.rect.x = 10
                ast1.y = random.randint(-100, -10)
                ast2.y = random.randint(-100, -10)
                ast3.y = random.randint(-100, -10)
                ast4.y = random.randint(-100, -10)
                SCORE = 0

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # обнуление данных и возврат размера экрана к размерам меню в случае выхода из игры
                if event.key == pygame.K_ESCAPE:
                    resize_screen((750, 500))
                    ship.rect.x = 10
                    ast1.y = random.randint(-100, -10)
                    ast2.y = random.randint(-100, -10)
                    ast3.y = random.randint(-100, -10)
                    ast4.y = random.randint(-100, -10)
                    return 'to menu'
                # пауза в случае нажатия Enter
                # и изменение размера игрового экрана согласно размерам экрана паузы
                if event.key == pygame.K_RETURN:
                    pause_screen(screen)
                    resize_screen(DISPLAY)

        ship.movement()  # движение игрока

        screen.blit(ship.image, ship.rect)
        pygame.display.update()
        pygame.time.delay(20)
        pygame.display.flip()
        pygame.display.update()

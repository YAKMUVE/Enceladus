import json
import random

import pygame.sprite

from db_worker import *
from win_screen import *
from game_over_screen import *
from pause import *
import time

# константы
DISPLAY = SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
FPS = 150
MOVE_SPEED = 7
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
win_sound = pygame.mixer.Sound('Sounds/win_sound.mp3')
lose_sound = pygame.mixer.Sound('Sounds/gameover_sound.mp3')


class Bullet(pygame.sprite.Sprite):  # класс пули
    def __init__(self, x: int, y: int, target_x: int, target_y: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

        # параметры цели
        self.target_x = target_x
        self.target_y = target_y

        # создание вектора до цели(определяется по позиции мышки игрока в функции shoot класса Player2)
        self.dir = pygame.math.Vector2(target_x - x, target_y - y)
        self.dir.scale_to_length(10)

    def update(self):
        # обновление объекта: если пуля выходит за рамки экрана, она уничтожается
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(self.rect):
            self.kill()
        self.movement()

    def movement(self):  # движение пули по вектору к цели
        self.rect.move_ip(self.dir)


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        with open('chosen_skin.json') as f:
            skin = json.load(f)
        self.image = pygame.image.load(skin)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 600, 500
        self.sound = pygame.mixer.Sound('Sounds/shoot_sound.mp3')

    def move(self):
        # движение объекта по всем осям со скоростью 8
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += 8
        if keys[pygame.K_a]:
            self.rect.x -= 8
        if keys[pygame.K_w]:
            self.rect.y -= 8
        if keys[pygame.K_s]:
            self.rect.y += 8

        # предотвращение выхода за рамки экрана
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):  # создание пули
        self.sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top, *pygame.mouse.get_pos())
        all_sprites.add(bullet)
        bullets.add(bullet)


class Entity(pygame.sprite.Sprite):  # класс сущности
    def __init__(self, lives):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/general/enemy.png')
        self.image = pygame.transform.smoothscale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 5)
        self.lives = lives

    def update(self):
        # обновление параметров сущности:
        # если у неё не осталось жизней, спрайт уничтожается, а к общему счету прибавляется гонорар,
        # также количество убитых сущностей увеличивается
        global entities_k, SCORE
        self.move_towards_player2(player)
        if self.lives < 0:
            self.kill()
            entities_k += 1
            SCORE += random.randint(1, 5)

    def move_towards_player2(self, player):
        # нахождение вектора между игроком и сущностью
        dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
                                      player.rect.y - self.rect.y)
        dirvect.normalize()
        # движение по вектору к игроку
        dirvect.scale_to_length(3)
        self.rect.move_ip(dirvect)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()


SCORE = 0  # текущий счет
entities_k = 0  # количество убитых сущностей

# создание групп спрайтов
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
entities = pygame.sprite.Group()
player = Player2()
all_sprites.add(player)


def create_entities():  # создание волны сущностей со случайными параметрами
    for i in range(random.randint(1, 5)):
        m = Entity(random.randint(20, 30))
        all_sprites.add(m)
        entities.add(m)


def run_lvl3():  # функция запуска основного цикла
    global entities_k, SCORE
    running = True
    while running:
        clock.tick(FPS)
        im = pygame.image.load('Sprites/backgrounds/lvl3_background.png')
        im = pygame.transform.scale(im, DISPLAY)
        screen.blit(im, (0, 0))
        player.move()

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # обнуление данных и возврат размера экрана к размерам меню в случае выхода из игры
                    resize_screen((750, 500))
                    all_sprites.remove(e for e in entities)
                    entities.empty()
                    entities_k = 0
                    SCORE = 0
                    return 'to menu'
                if event.key == pygame.K_SPACE:
                    # выстрел в случае нажатия пробела
                    player.shoot()
                if event.key == pygame.K_RETURN:
                    # пауза в случае нажатия Enter
                    # и изменение размера игрового экрана согласно размерам экрана паузы
                    pause_screen(screen)
                    resize_screen(DISPLAY)

        # отрисовка спрайтов
        all_sprites.draw(screen)
        all_sprites.update()

        # проверка на коллизию врага и пули: если она произошла, у сущности уменьшается количество жизней
        for e in entities:
            if pygame.sprite.spritecollide(e, bullets, False):
                e.lives -= 1

        # вызов экрана выигрыша, если убитых врагов больше 20
        # и сохранение заработанного счета
        if not(entities) and entities_k > 20:
            win_sound.play()
            with open('chosen_skin.json', 'w'):
                common_score = read_money()
            with open('money.json', 'w') as json_file:
                json.dump(common_score + SCORE, json_file)
            resize_screen((500, 500))
            w = win(screen, SCORE)
            database_changer('level', 4)

            entities_k = 0
            SCORE = 0
            all_sprites.remove(e for e in entities)
            entities.empty()
            return w

        # создание новой волны сущностей, если текущая отражена
        if not(entities):
            create_entities()

        # проверка на коллизию врага и игрока: если она произошла, вызов экрана проигрыша
        # и сохранение заработанного счета

        hit = pygame.sprite.spritecollide(player, entities, False)
        if hit:
            lose_sound.play()
            time.sleep(0.5)
            resize_screen((500, 500))
            m = main_gameover(screen)
            with open('chosen_skin.json', 'w'):
                common_score = read_money()
            with open('money.json', 'w') as json_file:
                json.dump(common_score + SCORE, json_file)

            entities_k = 0
            SCORE = 0
            all_sprites.remove(e for e in entities)
            entities.empty()
            if m == 'to menu':
                return 'to menu'
            else:
                # если игрок хочет попробовать еще раз, возвращение к начальным данным и параметрам
                player.rect.x = 500
                player.rect.y = 600
                resize_screen((1000, 800))

        all_sprites.draw(screen)
        pygame.display.flip()

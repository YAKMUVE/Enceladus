import random
import sqlite3 as sq
import time

from Point import Point
import pygame
import json
with open("money.json", "w") as f:
    f.write(json.dumps(0))

pygame.init()
screen = pygame.display.set_mode((700, 650), pygame.NOFRAME)
clock = pygame.time.Clock()

background_image = pygame.image.load('C:/Users/пк/Desktop/ПРОЕКТ_ИГРА/Sprites/backgrounds/lvl4_background.jpg')
background_image = pygame.transform.scale(background_image, (700, 650))
background_rect = background_image.get_rect()
all_sprites = pygame.sprite.Group()

progress = 0


def f():
    con = sq.connect('level_db.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS "levels" (
	"level"	INTEGER,
	"score"	INTEGER,
	"time"	INTEGER,
	"details"	INTEGER
);''')
    con.commit()
    con.close()


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
        elif keys[pygame.K_d] and ship.rect.x != 700:
            ship.rect.x += 5

    def collision_ast(self, ship):  # проверка коллизии с астероидами
        for i in asteroids:
            if ship.rect.collidepoint(i.x, i.y):
                return True
        return False

class FallingImage:  # класс астероида
    def __init__(self, x, y):
        #  подгузка изображения и его координат
        pic = pygame.image.load('Sprites/general/asteroid_pic.png')
        self.image = pygame.transform.scale(pic.convert_alpha(), (70, 70))
        self.x = x
        self.y = y


    def draw(self):  # отрисовка изображения астероида
        screen.blit(self.image, (self.x, self.y))




def pause():
    pause = pygame.Surface((600, 500), pygame.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    screen.blit(pause, (0, 0))


ast1, ast2, ast3, ast4 = FallingImage(400, 0), FallingImage(100, 0), FallingImage(200, 50), FallingImage(50, 0)
asteroids = [ast1, ast2, ast3, ast4]
points = [Point(10, 0), Point(100, 100), Point(250, 0)]

# списки координат объектов
c1 = [50, 80, 110, 150]
c2 = [200, 250, 300]
c3 = [350, 400, 450]
c4 = [500, 550]

cp = [i for i in range(10, 650, 100)]



def pos_cheker(arg, c):  # генерация новых случайных координат, если объект вышел за нижний предел экрана
    if arg.y > 600:
        arg.y = -100
        arg.x = random.choice(c)


ship = Spaseship()




def collision_point():  # проверка коллизии с поинтами
    for i in points:
        if ship.rect.collidepoint(i.x, i.y):
            return True
    return False


run = True
while run:
    clock.tick(55)
    screen.blit(background_image, (0, 0))
    for i in asteroids:
        i.draw()
    ast1.y += 3
    ast2.y += 6
    ast3.y += 4
    ast4.y += 5
    pos_cheker(ast1, c1)
    pos_cheker(ast2, c2)
    pos_cheker(ast3, c3)
    pos_cheker(ast4, c4)

    for p in points:
        p.draw(screen)
        p.y += 10
        pos_cheker(p, cp)
    if collision_ast():
        time.sleep(1.5)
        import game_over_screen
    if collision_point():
        progress += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RETURN:
                pause()
                time.sleep(3)

    ship.movement()

    screen.blit(ship.image, ship.rect)
    pygame.display.update()
    pygame.time.delay(20)
    pygame.display.flip()

    pygame.display.update()

pygame.quit()

import math

import pygame
import random

DISPLAY = SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
FPS = 60
MOVE_SPEED = 7
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/general/char_sprite_2.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.cooldown = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += 8
        if keys[pygame.K_a]:
            self.rect.x -= 8
        if keys[pygame.K_w]:
            self.rect.y -= 8
        if keys[pygame.K_s]:
            self.rect.y += 8
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def update(self):
        self.move()
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, lives):
        self.lives = lives

        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)

        pygame.sprite.Sprite.__init__(self)
        self.purposes = None
        self.speed = None

        self.width = 80
        self.height = 80

        self.image = pygame.image.load('Sprites/general/enemy.png')
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.c = self.rect.center
        self.x = x
        self.y = y

        # трекер движения
        self.upward = False
        self.downward = False
        self.leftward = False
        self.rightward = False

    def init_trajectory(self, speed: int, purposes: list):
        self.speed = speed
        self.purposes = purposes

    def update(self):
        self.move_towards_player2(player)

    def move_towards_player2(self, player):
        # нахождение вектора между игроком и сущностью
        dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
                                      player.rect.y - self.rect.y)
        dirvect.normalize()
        # движение по вектору к игроку
        dirvect.scale_to_length(3)
        self.rect.move_ip(dirvect)


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
entities = pygame.sprite.Group()
e = Entity(10, 20, 3)
entities.add(e)

bullets = pygame.sprite.Group()
running = True
while running:
    clock.tick(FPS)
    im = pygame.image.load('Sprites/backgrounds/lvl3_background.png')
    im = pygame.transform.scale(im, (DISPLAY))
    screen.blit(im, (0, 0))
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.draw(screen)
    all_sprites.update()
    entities.draw(screen)
    entities.update()
    hits = pygame.sprite.spritecollide(player, entities, False)
    if hits:
        running = False
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()

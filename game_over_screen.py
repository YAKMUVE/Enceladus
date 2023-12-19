import pygame
import sys

pygame.init()


class GameOverButton:
    def __init__(self, x, y, text):  # инициализация и подгрузка нужных элементов
        self.width = 200
        self.height = 60
        self.text = text
        self.pic = pygame.image.load('but1.jpg')
        self.hovered_pic = pygame.image.load('but2.jpg')
        self.pic = pygame.transform.scale(self.pic, (self.width, self.height))
        self.hovered_pic = pygame.transform.scale(self.hovered_pic, (self.width, self.height))

        self.rect = self.pic.get_rect(topleft=(x, y))
        self.rect = self.pic.get_rect(topleft=(x, y))

        self.hovered = False

    def drawer(self, screen):  # функция, отвечающая за вывод текста и соответствующей картинки
        picture = self.hovered_pic if self.hovered else self.pic
        screen.blit(picture, self.rect.topleft)

        font = pygame.font.SysFont('Ink Free', 36)
        font = font.render(self.text, True, (255, 255, 255))
        rect = font.get_rect(center=self.rect.center)
        screen.blit(font, rect)

    def hover_checker(self, pos):  # проверка наведения курсора на кнопку
        self.hovered = self.rect.collidepoint(pos)

    def eventor(self, event):  # обработка событий
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


w, h = 450, 450
screen = pygame.display.set_mode((w, h))

button1 = GameOverButton(100, 200, 'Play again', )
button2 = GameOverButton(100, 100, 'Main menu', )


def gameover():
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        button1.hover_checker(pygame.mouse.get_pos())
        button1.drawer(screen)
        button2.hover_checker(pygame.mouse.get_pos())
        button2.drawer(screen)
        pygame.display.flip()


gameover()

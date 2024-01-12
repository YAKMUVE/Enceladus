import pygame
import sys

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class GameOverButton:
    def __init__(self, x, y, width, height, text, sound_file):  # инициализация и подгрузка нужных элементов
        self.width = width
        self.height = height
        self.text = text
        self.sound = pygame.mixer.Sound(sound_file)

        self.image = pygame.image.load('Sprites/backgrounds/game_over_background.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.pic = pygame.image.load('but1.png')
        self.hovered_pic = pygame.image.load('but2.png')
        self.pic = pygame.transform.scale(self.pic, (self.width, self.height))
        self.hovered_pic = pygame.transform.scale(self.hovered_pic, (self.width, self.height))

        self.rect = self.pic.get_rect(topleft=(x, y))
        self.rect = self.pic.get_rect(topleft=(x, y))

        self.hovered = False

    def drawer(self, screen):  # функция, отвечающая за вывод текста и соответствующей картинки
        picture = self.hovered_pic if self.hovered else self.pic
        screen.blit(picture, self.rect.topleft)

        font = pygame.font.Font('Sprites/font/DischargePro.ttf', 36)
        font = font.render(self.text, True, WHITE)
        rect = font.get_rect(center=self.rect.center)
        screen.blit(font, rect)

    def hover_checker(self, pos):  # проверка наведения курсора на кнопку
        self.hovered = self.rect.collidepoint(pos)

    def eventor(self, event):  # обработка событий
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
            self.sound.play()
            return self.text


w, h = 500, 500
screen = pygame.display.set_mode((w, h), pygame.NOFRAME)


def write(screen):
    font = pygame.font.Font('Sprites/font/DischargePro.ttf', 70)
    t = font.render('Game over', True, WHITE)
    screen.blit(t, t.get_rect(center=(260, 100)))


def main_gameover():
    running = True
    background = pygame.image.load('Sprites/backgrounds/game_over_background.png')
    background = pygame.transform.scale(background, (w, h))

    play_again_btn = GameOverButton(150, 180, 200, 70, 'Play again', 'choice.mp3')
    ret_to_menu_btn = GameOverButton(150, 300, 200, 70, 'Main menu', 'choice.mp3')
    buttons = [play_again_btn, ret_to_menu_btn]

    while running:
        screen.blit(background, (0, 0))
        write(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for button in buttons:
                ev = button.eventor(event)
                if ev == 'Play again':
                    try_again()
                if ev == 'Main menu':
                    return_to_menu()
                    running = False

        for button in buttons:
            button.hover_checker(pygame.mouse.get_pos())
            button.drawer(screen)
        pygame.display.flip()


def try_again():
    pass


def return_to_menu():
    import main_menu


main_gameover()

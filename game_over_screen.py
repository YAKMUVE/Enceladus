import pygame

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class GameOverButton:  # класс кнопки
    def __init__(self, x, y, width, height, text, sound_file):  # инициализация и подгрузка нужных элементов
        self.width = width
        self.height = height
        self.text = text
        self.sound = pygame.mixer.Sound(sound_file)

        self.image = pygame.image.load('Sprites/backgrounds/game_over_background.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.pic = pygame.image.load('Sprites/general/but1.png')
        self.hovered_pic = pygame.image.load('Sprites/general/but2.png')
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


def write(screen):  # вывод текста
    font = pygame.font.Font('Sprites/font/DischargePro.ttf', 70)
    t1 = font.render('Game over', True, WHITE)
    screen.blit(t1, t1.get_rect(center=(260, 100)))


def main_gameover(screen):  # основной цикл экрана проигрыша
    running = True
    background = pygame.image.load('Sprites/backgrounds/game_over_background.png')
    background = pygame.transform.scale(background, (600, 800))

    # кнопки экрана проигрыша
    play_again_btn = GameOverButton(150, 150, 200, 70, 'Play again', 'choice.mp3')
    ret_to_menu_btn = GameOverButton(150, 270, 200, 70, 'Main menu', 'choice.mp3')
    buttons = [play_again_btn, ret_to_menu_btn]

    while running:
        screen.blit(background, (0, 0))
        write(screen)
        # обработка событий
        for event in pygame.event.get():
            for button in buttons:
                ev = button.eventor(event)
                if ev == 'Play again':
                    running = False
                if ev == 'Main menu':
                    return 'to menu'

        for button in buttons:
            button.hover_checker(pygame.mouse.get_pos())
            button.drawer(screen)
        pygame.display.flip()

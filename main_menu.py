import os

# установка позиции экрана
x = 200
y = 45
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

from main import *
from shop import *

from level3 import *
from level4 import *
import time

DISPLAY = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800


class ButtonMenu:  # класс кнопки
    def __init__(self, x, y, width, height, text, sound_file):
        # инициализация
        self.width = width
        self.height = height
        self.text = text
        self.passive_pic = pygame.image.load('Sprites/general/but1.png')
        self.active_pic = pygame.image.load('Sprites/general/but2.png')
        self.passive_pic = pygame.transform.scale(self.passive_pic, (self.width, self.height))
        self.active_pic = pygame.transform.scale(self.active_pic, (self.width, self.height))

        self.rect = self.passive_pic.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound(sound_file)
        self.hovered = False

    def drawer(self, sc):  # вывод текста на экран
        sc.blit(self.active_pic if self.hovered else self.passive_pic, self.rect.topleft)
        font = pygame.font.Font('Sprites/font/DischargePro.ttf', 36)
        text_rendered = font.render(self.text, True, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=self.rect.center)
        sc.blit(text_rendered, text_rect)

    def hover_checker(self, pos):  # проверка наведения мыши на кнопку
        self.hovered = self.rect.collidepoint(pos)

    def eventor(self, event):  # проверка нажатия на кнопку
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.sound.play()
            return self.text


flag = 0
pygame.init()
w, h = 750, 500
screen = pygame.display.set_mode((w, h), pygame.NOFRAME, pygame.RESIZABLE)


def main_menu():  # функция запуска основного цикла меню
    global w, h

    background = pygame.image.load('Sprites/backgrounds/menu_background.JPG')
    background = pygame.transform.scale(background, (w, h))

    # кнопки меню
    newgame_btn = ButtonMenu(230, 100, 240, 70, 'New game', 'choice.mp3')
    continue_btn = ButtonMenu(230, 200, 240, 70, 'Continue', 'choice.mp3')
    shop_btn = ButtonMenu(230, 300, 240, 70, 'Shop', 'choice.mp3')
    reference_btn = ButtonMenu(650, 410, 70, 70, '?', 'choice.mp3')
    player_btn = ButtonMenu(650, 10, 70, 70, 'Me', 'choice.mp3')
    quit_btn = ButtonMenu(230, 400, 240, 70, 'Quit', 'choice.mp3')
    buttons = [newgame_btn, continue_btn, shop_btn, reference_btn, player_btn, quit_btn]

    running = True
    while running:
        json_checker()
        screen.blit(background, (0, 0))
        write(screen)
        # обработка событий, вызов функций соответствующих разделов
        for event in pygame.event.get():
            for button in buttons:
                ev = button.eventor(event)

                # выход из игры если нажата кнопка "Quit"
                if ev == 'Quit':
                    time.sleep(1)
                    running = False

                # переход в раздел управления если нажата кнопка "?"
                if ev == '?':
                    reference()

                # сброс прогресса если нажата кнопка "New game"
                if ev == 'New game':
                    if not (new_game()):
                        time.sleep(1)

                # продолжить игру если нажата кнопка "Continue"
                if ev == 'Continue':
                    database_maker()
                    resize_screen(DISPLAY)

                    # определение текущего уровня и запуск функции основного цикла уровня
                    cur_lvl = level_determinant()
                    if cur_lvl == 5:
                        database_changer('level', 1)
                        cur_lvl = 1
                    if cur_lvl == 1 or cur_lvl == 2:
                        with open('chosen_skin.json') as f:
                            skin = json.load(f)
                        r = common_lvl_run(Player(535, 750, skin))
                    if cur_lvl == 3:
                        resize_screen((1000, 800))
                        r = run_lvl3()
                    if cur_lvl == 4:
                        resize_screen((700, 650))
                        r = run_lvl4()
                    if r == 'to menu':
                        resize_screen((w, h))

                # переход в раздел информации об игроке если нажата кнопка "Me"
                if ev == 'Me':
                    me()

                # переход в магазин если нажата кнопка 'Shop'
                if ev == 'Shop':
                    resize_screen((500, 700))
                    main_shop()

        # рендеринг
        read_money()
        for button in buttons:
            button.hover_checker(pygame.mouse.get_pos())
            button.drawer(screen)
        pygame.display.flip()


def reference():  # раздел информации об управлении
    text = ['Left: A', ' Right:  D', 'Up: W', 'Down: S', 'Exit: Esc', 'Pause: Enter', 'Shoot: Space']
    background = pygame.image.load('Sprites/backgrounds/background_menu_2.jpg')
    background = pygame.transform.scale(background, (w, h))
    # кнопка возврата
    back_btn = ButtonMenu(255, 380, 240, 70, 'Back', 'choice.mp3')
    font = pygame.font.Font('Sprites/font/DischargePro.ttf', 30)

    running = True
    while running:
        # вывод текста
        screen.blit(background, (0, 0))
        y = 40
        for i in text:
            t = font.render(i, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=(380, y)))
            y += 50

        # обработка событий - возврат в меню
        for event in pygame.event.get():
            ev = back_btn.eventor(event)
            if ev == 'Back':
                running = False

        # рендеринг
        back_btn.hover_checker((pygame.mouse.get_pos()))
        back_btn.drawer(screen)
        pygame.display.flip()


def new_game():  # раздел новой игры
    background = pygame.image.load('Sprites/backgrounds/background_menu_2.jpg')
    background = pygame.transform.scale(background, (w, h))

    # кнопки yes и no
    ok_btn = ButtonMenu(250, 200, 240, 70, 'Yes', 'choice.mp3')
    cancel_btn = ButtonMenu(250, 300, 240, 70, 'No', 'choice.mp3')
    buttons = [ok_btn, cancel_btn]

    running = True
    while running:
        screen.blit(background, (0, 0))
        # вывод текста
        font = pygame.font.Font('Sprites/font/DischargePro.ttf', 36)
        t1 = font.render('Are you sure you want to start a new game?', True, (255, 255, 255))
        t2 = font.render('Current progress will be deleted.', True, (255, 255, 255))
        screen.blit(t1, t1.get_rect(center=(380, 100)))
        screen.blit(t2, t2.get_rect(center=(380, 130)))
        f = 1

        # обработка событий
        for event in pygame.event.get():
            for button in buttons:
                ev = button.eventor(event)
                # возврат в меню если нажата кнопка no,
                if ev == 'No':
                    return True
                # иначе удаление прогресса.
                if ev == 'Yes':
                    delete_progress()
                    return False

        # рендеринг
        for button in buttons:
            button.hover_checker(pygame.mouse.get_pos())
            button.drawer(screen)
        if not (f):
            time.sleep(1.5)
            return 'deleted'
        pygame.display.flip()


def me():  # раздел информации об игроке
    text = ['general: Ace', 'location: Enceladus', 'citizenship: american', f'count: {read_money()}']
    background = pygame.image.load('Sprites/backgrounds/background_menu_2.jpg')
    background = pygame.transform.scale(background, (w, h))
    # кнопка возврата
    back_btn = ButtonMenu(255, 380, 240, 70, 'Back', 'choice.mp3')
    font = pygame.font.Font('Sprites/font/DischargePro.ttf', 36)

    running = True
    while running:
        screen.blit(background, (0, 0))
        y = 50
        for i in text:
            t = font.render(i, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=(380, y)))
            y += 50

        # возврат в меню при нажатии кнопки Back
        for event in pygame.event.get():
            ev = back_btn.eventor(event)
            if ev == 'Back':
                running = False

        # рендеринг
        back_btn.hover_checker((pygame.mouse.get_pos()))
        back_btn.drawer(screen)
        pygame.display.flip()


def write(sc):  # вывод текста
    font = pygame.font.Font('Sprites/font/DischargePro.ttf', 60)
    t = font.render('Enceladus', True, (255, 255, 255))
    sc.blit(t, t.get_rect(center=(145, 30)))


def delete_progress():  # удаление прогресса игры
    try:
        os.remove('NEW.db')
    except FileNotFoundError:
        return False


main_menu()

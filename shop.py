import json

import pygame.mouse

from db_worker import *

pygame.init()
w, h = 500, 700
screen = pygame.display.set_mode((w, h), pygame.NOFRAME, pygame.RESIZABLE)
json_checker()
with open('chosen_skin.json', 'r') as json_file:
    SKIN = json.load(json_file)


class ButtonSprite:  # класс кнопки
    def __init__(self, x, y, text, pas_img, act_img, number, price):
        # инициализация
        global SKIN
        self.pic = pas_img
        self.number = number
        self.price = price
        self.width = 70
        self.height = 70
        self.text = text
        self.passive_pic = pygame.image.load(pas_img)
        self.active_pic = pygame.image.load(act_img)
        self.passive_pic = pygame.transform.scale(self.passive_pic, (self.width, self.height))
        self.active_pic = pygame.transform.scale(self.active_pic, (self.width, self.height))

        self.rect = self.passive_pic.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound('choice.mp3')
        self.hovered = False

    def hover_checker(self, pos):  # проверка наведения мыши на кнопку
        self.hovered = self.rect.collidepoint(pos)

    def drawer(self, sc, cent):  # вывод текста на экран
        sc.blit(self.active_pic if self.hovered else self.passive_pic, self.rect.topleft)
        font = pygame.font.Font('Sprites/font/DischargePro.ttf', 36)
        text_rendered = font.render(self.text, True, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=cent)
        sc.blit(text_rendered, text_rect)

    def eventor(self, event):  # проверка нажатия на кнопку
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.sound.play()
            return self.number


class Button:  # класс кнопки
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
            return True


def purchase(price, n):  # функция покупки скина
    with open("money.json", "r") as json_file:
        money = json.load(json_file)
    if price <= money:
        money -= price
        with open('money.json', 'w') as json_file:
            json.dump(money, json_file)
            buy_sk(n)
        return True
    else:
        return False


centers = [(250, 130), (245, 275), (250, 410)]


def main_shop():  # функция запуска основного цикла
    global w, h
    background = pygame.image.load('Sprites/backgrounds/shop_background.png')
    background = pygame.transform.scale(background, (w, h))

    back_btn = Button(140, 580, 240, 70, 'Back', 'choice.mp3')
    ace1 = ButtonSprite(220, 170, 'traditional Ace', 'Sprites/general/classic_ace.png',
                        'Sprites/general/classic_ace2.png', 1, 0)
    ace2 = ButtonSprite(220, 310, 'infernal Ace', 'Sprites/general/infernal_ace.png',
                        'Sprites/general/infernal_ace2.png', 2, 150)
    ace3 = ButtonSprite(220, 450, 'star guardian Ace', 'Sprites/general/star_guardian_ace.png',
                        'Sprites/general/star_guardian_ace2.png', 3, 300)

    buttons = [ace1, ace2, ace3]

    running = True
    while running:
        screen.blit(background, (0, 0))
        write(screen)
        for event in pygame.event.get():
            for button in buttons:
                ev = button.eventor(event)
                if ev:
                    status = bought_skin(button.number)
                    if status == 'yes':
                        skin_choice(button.pic)
                    else:
                        buy(button.price, button.number, button.pic)
            if back_btn.eventor(event):
                resize_screen((750, 500))
                running = False

        i = 0
        for button in buttons:
            button.hover_checker(pygame.mouse.get_pos())
            button.drawer(screen, centers[i])
            i += 1
        back_btn.hover_checker(pygame.mouse.get_pos())
        back_btn.drawer(screen)

        pygame.display.flip()


def buy(pr, number, skin):  # функция раздела покупки
    global SKIN
    background = pygame.image.load('Sprites/backgrounds/lvl4_background.jpg')
    background = pygame.transform.scale(background, (w, h))

    ok_btn = Button(140, 300, 240, 70, 'Yes', 'choice.mp3')
    cancel_btn = Button(140, 420, 240, 70, 'No', 'choice.mp3')

    running = True
    while running:
        screen.blit(background, (0, 0))

        font = pygame.font.Font('Sprites/font/DischargePro.ttf', 36)

        t1 = font.render('Do you want to', True, (255, 255, 255))
        t2 = font.render(f'buy this skin for {pr}?', True, (255, 255, 255))
        screen.blit(t1, t1.get_rect(center=(250, 120)))
        screen.blit(t2, t2.get_rect(center=(250, 200)))

        # обработка событий - если нажата кнопка yes, совершается покупка скина и автоматический выбор
        for event in pygame.event.get():
            if ok_btn.eventor(event):
                p = purchase(pr, number)
                if p:
                    SKIN = skin
                    with open("chosen_skin.json", "w") as json_file:
                        json.dump(SKIN, json_file)
                running = False
            if cancel_btn.eventor(event):
                running = False

        # рендеринг
        ok_btn.hover_checker(pygame.mouse.get_pos())
        cancel_btn.hover_checker(pygame.mouse.get_pos())
        ok_btn.drawer(screen)
        cancel_btn.drawer(screen)
        pygame.display.flip()


def skin_choice(skin):  # функция раздела выбора скина
    global SKIN

    background = pygame.image.load('Sprites/backgrounds/lvl4_background.jpg')
    background = pygame.transform.scale(background, (w, h))
    yes_btn = Button(140, 300, 240, 70, 'Yes', 'choice.mp3')
    cancel_btn = Button(140, 420, 240, 70, 'No', 'choice.mp3')
    font = pygame.font.Font('Sprites/font/DischargePro.ttf', 50)

    running = True
    while running:
        screen.blit(background, (0, 0))
        t1 = font.render('Do you want to', True, (255, 255, 255))
        t2 = font.render('choose this skin?', True, (255, 255, 255))
        screen.blit(t1, t1.get_rect(center=(250, 120)))
        screen.blit(t2, t2.get_rect(center=(250, 200)))

        # обработка событий - если нажата кнопка yes, совершается выбор скина
        for event in pygame.event.get():
            if cancel_btn.eventor(event):
                running = False
            if yes_btn.eventor(event):
                SKIN = skin
                with open("chosen_skin.json", "w") as json_file:
                    json.dump(SKIN, json_file)
                running = False

        # рендеринг
        yes_btn.hover_checker((pygame.mouse.get_pos()))
        yes_btn.drawer(screen)
        cancel_btn.hover_checker((pygame.mouse.get_pos()))
        cancel_btn.drawer(screen)
        pygame.display.flip()


def write(sc):  # вывод текста на экран
    with open("money.json", "r") as json_file:
        money = json.load(json_file)
    font = pygame.font.Font('Sprites/font/DischargePro.ttf', 60)
    t = font.render(f'Money: {money}', True, (255, 255, 255))
    sc.blit(t, t.get_rect(center=(130, 30)))

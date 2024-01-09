import pygame


class ButtonMenu:
    def __init__(self, x, y, width, height, text, sound_file):
        self.width = width
        self.height = height
        self.text = text
        self.passive_pic = pygame.image.load('but2.JPG')
        self.active_pic = pygame.image.load('but1.JPG')
        self.passive_pic = pygame.transform.scale(self.passive_pic, (self.width, self.height))
        self.active_pic = pygame.transform.scale(self.active_pic, (self.width, self.height))

        self.rect = self.passive_pic.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound(sound_file)
        self.hovered = False

    def drawer(self, screen):
        screen.blit(self.active_pic if self.hovered else self.passive_pic, self.rect.topleft)
        font = pygame.font.SysFont('Better VCR Regular', 36)
        text_rendered = font.render(self.text, True, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=self.rect.center)
        screen.blit(text_rendered, text_rect)

    def hover_checker(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def eventor(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.sound.play()


class ShopWindow:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('shop_background.png')
        self.background = pygame.transform.scale(self.background, (700, 700))

        # Кнопки покупки скинов
        self.items = [
            ButtonMenu(100, 100, 200, 50, 'Инфернальный Эйс\n Купить [Цена]', 'buy_sound.mp3'),
            ButtonMenu(100, 100, 200, 50, 'Традиционный Эйс\n Купить [Цена]', 'buy_sound.mp3'),
            ButtonMenu(100, 100, 200, 50, 'Боец галактики Эйс\n Купить [Цена]', 'buy_sound.mp3')
        ]
        self.return_button = ButtonMenu(550, 600, 150, 50, 'Вернуться в меню', 'back.mp3')

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                pos = pygame.mouse.get_pos()
                for item in self.items:
                    item.hover_checker(pos)
                    item.eventor(event)
                self.return_button.hover_checker(pos)
                self.return_button.eventor(event)

            for item in self.items:
                item.drawer(self.screen)
            self.return_button.drawer(self.screen)

            pygame.display.flip()


def main_menu():
    pygame.init()
    w, h = 700, 700
    screen = pygame.display.set_mode((w, h))
    background = pygame.image.load('menu_background.JPG')
    background = pygame.transform.scale(background, (w, h))

    buttons = [
        ButtonMenu(100, 100, 200, 50, 'Shop', 'choice.mp3'),
    ]

    running = True
    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.hover_checker(pygame.mouse.get_pos())
                button.eventor(event)

        for button in buttons:
            if button == shop_button and button.hovered:
                ShopWindow(screen).run()
            else:
                button.drawer(screen)

        pygame.display.flip()

    pygame.quit()


main_menu()

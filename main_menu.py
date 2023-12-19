import pygame


class ButtonMenu:
    def __init__(self, x, y, width, height, text):
        self.width = width
        self.height = height
        self.text = text
        self.passive_pic = pygame.image.load('but2.JPG')
        self.active_pic = pygame.image.load('but1.JPG')
        self.passive_pic = pygame.transform.scale(self.passive_pic, (self.width, self.height))
        self.active_pic = pygame.transform.scale(self.active_pic, (self.width, self.height))

        self.rect = self.passive_pic.get_rect(topleft=(x, y))
        self.hovered = False

    def drawer(self, screen):
        screen.blit(self.active_pic if self.hovered else self.passive_pic, self.rect.topleft)
        font = pygame.font.SysFont('Ink Free', 36)
        text_rendered = font.render(self.text, True, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=self.rect.center)
        screen.blit(text_rendered, text_rect)

    def hover_checker(self, pos):
        self.hovered = self.rect.collidepoint(pos)


def main_menu():
    pygame.init()
    w, h = 700, 500
    screen = pygame.display.set_mode((w, h))
    background = pygame.image.load('menu_background.JPG')
    background = pygame.transform.scale(background, (w, h))

    buttons = [
        ButtonMenu(100, 100, 200, 50, 'Shop'),
    ]

    running = True
    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.hover_checker(pygame.mouse.get_pos())

        for button in buttons:
            button.drawer(screen)

        pygame.display.flip()

    pygame.quit()


main_menu()

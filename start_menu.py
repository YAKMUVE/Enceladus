import pygame
import sys

pygame.init()


class ButtonMenu:
    def __init__(self, x, y, text):
        self.width = 20
        self.height = 20
        self.text = text
        self.pic = pygame.image.load('but1.png')
        self.hovered_pic = pygame.image.load('but2.png')
        self.pic = pygame.transform.scale(self.pic, (self.width, self.height))
        self.hovered_pic = pygame.transform.scale(self.hovered_pic, (self.width, self.height))

        self.rect = self.pic.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound('choice.mp3')
        self.rect = self.pic.get_rect(topleft=(x, y))

        self.hovered = False

    def drawer(self, screen):
        picture = self.hovered_pic if self.hovered else self.pic
        screen.blit(self.pic, self.rect.topleft)
        font = pygame.font.SysFont('Ink Free', 36)
        font = font.render(self.text, True, (255, 255, 255))
        rect = font.get_rect(center=self.rect.center)
        screen.blit(font, rect)

    def hover_checker(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def eventor(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


w, h = 700, 700
screen = pygame.display.set_mode((w, h))

button = ButtonMenu(100, 100, 'shop',)


def main_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        button.hover_checker(pygame.mouse.get_pos())
        button.drawer(screen)
        pygame.display.flip()

main_menu()

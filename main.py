import sys

import pygame
from pygame.locals import QUIT


class Object:
    def __init__(self, width: int, height: int, path: str, x: int, y: int):
        self.width = width
        self.height = height

        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def rotate(self, degrees: int):
        self.image = pygame.transform.rotate(self.image, degrees)


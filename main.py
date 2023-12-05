import pygame


# объявление const
SIZE = WIDTH, HEIGHT = 800, 600
FPS = 60

# инициализация
pygame.init()

# подготовка переменных
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()


class Object(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, path: str, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
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


if __name__ == '__main__':
    while pygame.event.wait().type != pygame.quit():
        # обновление
        sprites.update()

        # рендеринг
        screen.fill((0, 0, 0))
        sprites.draw(screen)

        # вывод
        pygame.display.flip()

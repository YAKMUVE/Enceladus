import pygame
import random


class Level2:
    def __init__(self):
        pygame.init()
        size = (650, 650)
        self.screen_width = 600
        self.screen_height = 650
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Level 2')
        self.color = '#ffffff'
        self.background_image = pygame.image.load('level_background.png')
        self.background_image = pygame.transform.scale(self.background_image, size)
        self.landed = 0

        self.screen.blit(self.background_image, (0, 0))
        pygame.display.flip()

        self.snowflakes = []
        self.snow_per_pixel = 250
        self.level_height = 0

        self.clock = pygame.time.Clock()

    def add_drop(self):
        self.snowflakes.append([random.randint(0, self.screen_width), 0])

    # рисование снежинок
    def snowflake_painter(self):
        for i in self.snowflakes:
            pygame.draw.line(self.screen, self.color, (i[0], i[1]), (i[0], i[1] + 2), 3)

    # подъем уровня
    def update_drops(self):
        for i in self.snowflakes:
            i[1] += 5
            if i[1] >= self.screen_height:
                self.snowflakes.remove(i)
                self.landed += 10
                if self.landed % self.snow_per_pixel == 0:
                    self.level_height += 3

    # рисование уровня снега
    def level_painter(self):
        pygame.draw.rect(self.screen, self.color,
                         (0, self.screen_height - self.level_height, self.screen_width, self.level_height))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.add_drop()
            self.update_drops()
            self.screen.blit(self.background_image, (0, 0))
            self.snowflake_painter()
            self.level_painter()
            pygame.display.update()
            self.clock.tick(35)

        pygame.quit()


if __name__ == "__main__":
    app = Level2()
    app.run()

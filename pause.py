import pygame

pygame.font.init()

WHITE = (255, 255, 255)


def write(screen):  # вывод текста
    font1 = pygame.font.Font('Sprites/font/DischargePro.ttf', 100)
    t1 = font1.render('Pause', True, WHITE)
    screen.blit(t1, t1.get_rect(center=(245, 100)))

    font2 = pygame.font.Font('Sprites/font/DischargePro.ttf', 60)
    t2 = font2.render('Return to game:', True, WHITE)
    screen.blit(t2, t2.get_rect(center=(250, 250)))

    t3 = font2.render('Enter', True, WHITE)
    screen.blit(t3, t3.get_rect(center=(250, 350)))


def pause_screen(screen):  # вызов экрана паузы
    screen = pygame.display.set_mode((500, 500), pygame.NOFRAME, pygame.RESIZABLE)
    background = pygame.image.load('Sprites/backgrounds/lvl4_background.jpg')
    background = pygame.transform.scale(background, (500, 500))
    run = True
    while run:
        screen.blit(background, (0, 0))
        write(screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                run = False
        pygame.display.flip()

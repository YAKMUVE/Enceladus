import pygame
from game_over_screen import GameOverButton
screen = pygame.display.set_mode((500, 500), pygame.NOFRAME)


def write(screen, points):  # вывод текста
    font = pygame.font.Font('Sprites/font/DischargePro.ttf', 70)
    t1 = font.render('You win!', True, (255, 255, 255))
    screen.blit(t1, t1.get_rect(center=(260, 100)))

    t2 = font.render(f'score: +{points} points', True, (255, 255, 255))
    screen.blit(t2, t2.get_rect(center=(260, 380)))


def win(screen, points):  # основной цикл экрана выигрыша
    running = True
    background = pygame.image.load('Sprites/backgrounds/game_over_background.png')
    background = pygame.transform.scale(background, (600, 800))

    ret_to_menu_btn = GameOverButton(150, 200, 200, 70, 'Main menu', 'choice.mp3')


    while running:
        screen.blit(background, (0, 0))
        write(screen, points)
        for event in pygame.event.get():
            ev = ret_to_menu_btn.eventor(event)
            if ev == 'Main menu':
                return 'to menu'

        ret_to_menu_btn.hover_checker(pygame.mouse.get_pos())
        ret_to_menu_btn.drawer(screen)
        pygame.display.flip()


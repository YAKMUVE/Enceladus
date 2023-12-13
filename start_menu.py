import menu as menu
import pygame
import pygame_menu
from pygame_menu import Theme

pygame.init()
surface = pygame.display.set_mode((700, 700))

size = (700, 700)


def set_difficulty(value, difficulty):
    # Do the job here !
    pass


def start_the_game():
    # Do the job here !
    pass



titlefont = pygame.font.SysFont('Ink Free', 50)
widgetfont = pygame.font.SysFont('Ink Free', 45)
theme = Theme(background_color='#b3deff',
              widget_font_color='#1581e6',
              widget_font=widgetfont,
              widget_font_shadow=True,
              widget_font_shadow_color='#102747',
              widget_padding=20)
menu = pygame_menu.Menu('', 700, 700,
                        theme=theme)


menu.add.button('Shop', start_the_game)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)

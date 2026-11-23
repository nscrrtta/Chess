import pygame
pygame.init()

from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game.renderer import Renderer as GameRenderer
from menu.renderer import Renderer as MenuRenderer
from game.game import Game
from menu.menu import Menu


pygame.display.set_caption('Chess by Nick Sciarretta')

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

game = Game()
menu = Menu(game)

game_renderer = GameRenderer(window, game)
menu_renderer = MenuRenderer(window, menu)

clock = pygame.time.Clock()

running = True
while running:
    elapsed = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            menu.toggle_active()
        elif menu.active:
            menu.handle_event(event)
        else:
            game.handle_event(event)

    game.tick_clock(elapsed)

    if menu.result != game.result:
        menu.result = game.result
        menu_renderer._update_text()
        # Open the menu when the game ends, close it when a new game starts
        if menu.active != game.game_over():
            menu.toggle_active()

    game_renderer.draw()
    if menu.active:
        menu_renderer.draw()

    pygame.display.update()

pygame.quit()

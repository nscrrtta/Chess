from utils.constants import *
from utils.common import *

from menu.constants import *
from menu.rect import ClickableRect
from menu.number import NumberInput
from menu.clock import ClockInput
from menu.button import Button
from menu.menu import Menu

import pygame


class Renderer:

    # Border radius of rects
    radius = int_scale(10)

    # Game result, score and Fischer Random label
    large_font = Font(86)
    small_font = Font(42)
    score_font = Font(45)
    frand_font = Font(38)

    rect = pygame.Rect(
        SQUARE_SIZE + BOARD_OFFSET_X,
        SQUARE_SIZE + BOARD_OFFSET_Y,
        SQUARE_SIZE * 6,
        SQUARE_SIZE * 6
    )

    def __init__(self, window: pygame.Surface, menu: Menu):
        self.window = window
        self.menu = menu
        self.game = menu.game

        # Surface for drawing transparent shapes
        self.surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surf.fill(Colours.grey(60))
        self.surf.set_alpha(120)

        # Images
        self.images = [
            self._image('wp_lg', MENU_WHITE_PAWN_LG),
            self._image('bp_lg', MENU_BLACK_PAWN_LG),
            self._image('wp_sm', MENU_WHITE_PAWN_SM),
            self._image('bp_sm', MENU_BLACK_PAWN_SM),
        ]
        self.checkmark = self._image('checkmark', MENU_CHECKBOX)

        self._update_text()

    def draw(self):
        # Fill screen with transparent grey rectangle
        self.window.blit(self.surf, (0, 0))

        # Grey square with 1px black border in center of window
        pygame.draw.rect(self.window, Colours.grey(100), self.rect, 0, self.radius * 2)
        pygame.draw.rect(self.window, Colours.black, self.rect, 1, self.radius * 2)

        # Buttons
        self._draw_button(self.menu.new_game_btn)
        self._draw_button(self.menu.new_position_btn)
        self._draw_checkbox(self.menu.fischer_checkbox)

        # Images
        for image in self.images:
            self.window.blit(image.surf, image.rect)
        if self.menu.fischer_checkbox.pressed:
            self.window.blit(self.checkmark.surf, self.checkmark.rect)

        for text in self.text:
            self.window.blit(text.surf, text.rect)

        # Clocks
        self._draw_clock_input(self.menu.white_clock)
        self._draw_clock_input(self.menu.black_clock)

    def _draw_button(self, button: Button):
        # Draw two rectangles to create a button that looks 3D
        colour = Colours.button_bot if button.enabled else Colours.grey(90)
        pygame.draw.rect(self.window, colour, button.bot_rect, 0, self.radius)

        colour = Colours.button_top if button.enabled else Colours.grey(180)
        pygame.draw.rect(self.window, colour, button.rect, 0, self.radius)

        # Text in center of top rectangle
        self.window.blit(button.text.surf, button.text.rect)

    def _draw_checkbox(self, checkbox: ClickableRect):
        # Grey rectangle with 1px black border
        pygame.draw.rect(self.window, Colours.grey(180), checkbox.rect, 0, self.radius)
        pygame.draw.rect(self.window, Colours.black, checkbox.rect, 1, self.radius)

    def _draw_clock_input(self, clock: ClockInput):
        for text in clock.text:
            self.window.blit(text.surf, text.rect)
        for number_input in clock.inputs:
            self._draw_number_input(number_input)

    def _draw_number_input(self, number_input: NumberInput):
        colour = Colours.grey(160) if number_input.pressed else Colours.grey(120)
        pygame.draw.rect(self.window, colour, number_input.rect, 0, self.radius)
        self.window.blit(number_input.text.surf, number_input.text.rect)

    def _update_text(self):
        colour = 'Black' if self.game.curr_player.white else 'White'

        # Large and small text (game result)
        large, small = MENU_RESULT_TEXT[self.game.result]
        large = large.format(colour=colour)

        # Score text
        w = self.game.white_player.score
        b = self.game.black_player.score
        score = f'{w} - {b}'

        frand = 'Fischer Random'

        self.text = [
            self._text(self.large_font, large, MENU_LARGE_TEXT),
            self._text(self.small_font, small, MENU_SMALL_TEXT),
            self._text(self.score_font, score, MENU_SCORE_TEXT),
            self._text(self.frand_font, frand, MENU_FRAND_TEXT)
        ]

    def _text(self, font: Font, text: str, center: Point) -> Surface:
        return Surface(font.render(text), center=center)

    def _image(self, file_name: str, center: Point) -> Surface:
        return Surface(Images.get(file_name), center=center)

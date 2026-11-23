from game.player import Player
from game.game import Game

from menu.constants import *
from menu.rect import ClickableRect
from menu.number import NumberInput
from menu.clock import ClockInput
from menu.button import Button

import pygame


class Menu:

    def __init__(self, game: Game):
        self.game = game

        # main.py compares this with the game result.
        # When the two differ, the menu is toggled.
        self.result = None

        # Menu is displayed when self.active = True
        self.active = False

        # Starts a new game
        self.new_game_btn = Button(MENU_NEW_GAME, text='New Game')

        # Creates a new Fischer Random position, then starts a new game
        self.new_position_btn = Button(MENU_NEW_POSITION, text='New Position')
        self.new_position_btn.enabled = False

        self.buttons = [self.new_game_btn, self.new_position_btn]

        # If checked - New Position button is enabled
        # If New Game button is pressed while checked,
        # game will start with current fischer random position
        self.fischer_checkbox = ClickableRect(MENU_CHECKBOX, 30, 30)

        # Input fields for clocks
        self.white_clock = ClockInput(MENU_WHITE_CLOCK)
        self.black_clock = ClockInput(MENU_BLACK_CLOCK)

        self.number_inputs = self.white_clock.inputs + self.black_clock.inputs
        self.focused_input: NumberInput | None = None

    def toggle_active(self):
        self.active = not self.active
        self.new_position_btn.depress()
        self.new_game_btn.depress()
        if self.focused_input is not None:
            self.focused_input.leave_focus()
            self.focused_input = None
        self.game._drop_held_piece()

    def new_game(self):
        self._set_clock(self.white_clock, self.game.white_player)
        self._set_clock(self.black_clock, self.game.black_player)

        new_position = self.new_position_btn.pressed
        fischer_random = self.fischer_checkbox.pressed
        self.game.new_game(new_position, fischer_random)

        self.toggle_active()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_down(*event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse_up()
        elif event.type == pygame.MOUSEMOTION:
            self._mouse_motion(*event.pos)
        elif event.type == pygame.KEYDOWN:
            self._key_down(event.key)

    def _mouse_down(self, x: int, y: int):
        # Clicked either button to start a new game
        for button in self.buttons:
            if button.enabled and button.clicked(x, y):
                button.press()
                return

        # Clicked Fischer Random checkbox
        if self.fischer_checkbox.clicked(x, y):
            checkbox = self.fischer_checkbox
            checkbox.pressed = not checkbox.pressed

            button = self.new_position_btn
            button.enabled = checkbox.pressed
            return

        if self.focused_input is not None:
            # Clicked active number input -> no action
            if self.focused_input.clicked(x, y):
                return

            # Clicked out of active number input
            self.focused_input.leave_focus()
            self.focused_input = None

        # Clicked new number input
        for number_input in self.number_inputs:
            if number_input.clicked(x, y):
                self.focused_input = number_input
                number_input.pressed = True
                return

    def _mouse_up(self):
        if self.buttons[0].pressed or self.buttons[1].pressed:
            self.new_game()

    def _mouse_motion(self, x: int, y: int):
        for button in self.buttons:
            if button.pressed and not button.clicked(x, y):
                button.depress()

    def _key_down(self, key: int):
        if key == pygame.K_TAB:
            self._tab_through_number_inputs()
        elif self.focused_input is None:
            return
        elif key == pygame.K_BACKSPACE:
            self.focused_input.remove_number()
        elif pygame.K_0 <= key <= pygame.K_9:
            self.focused_input.input_number(key - pygame.K_0)

    def _tab_through_number_inputs(self):
        i = 0
        if self.focused_input is not None:
            i = self.number_inputs.index(self.focused_input)
            i = (i + 1) % len(self.number_inputs)
            self.focused_input.leave_focus()

        self.focused_input = self.number_inputs[i]
        self.focused_input.pressed = True

    def _set_clock(self, clock: ClockInput, player: Player):
        seconds = clock.get_seconds()
        increment = clock.get_increment()
        player.clock.reset(seconds, increment)

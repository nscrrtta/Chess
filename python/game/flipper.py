from utils.constants import TOP_CENTER, BOT_CENTER
from game.captured import Captured
from game.player import Player
from game.view import View
import pygame


class Flipper:

    def __init__(self, white: Player, black: Player, captured: Captured):
        self.pieces = white.pieces + black.pieces + white.promos + black.promos
        self.clocks = [white.clock, black.clock]
        self.captured = captured

    def flip(self):
        View.flipped = not View.flipped
        self._flip_pieces()
        self._flip_clocks()
        self._flip_captured_pieces()

    def _flip_pieces(self):
        for piece in self.pieces:
            if not piece.held:
                piece._update_xy()

    def _flip_clocks(self):
        for clock in self.clocks:
            self._flip_rect(clock.rect)
            self._flip_rect(clock.text.rect)
            self._flip_rect(clock.image.rect)
            self._flip_rect(clock.transparent.rect)

    def _flip_captured_pieces(self):
        for image in self.captured.images:
            self._flip_rect(image.rect)
        self._flip_rect(self.captured.text.rect)

    def _flip_rect(self, rect: pygame.Rect):
        if rect.centery == TOP_CENTER:
            rect.centery = BOT_CENTER
        else:
            rect.centery = TOP_CENTER

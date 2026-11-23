from utils.common import Sounds

from game.captured import Captured, CapturedSnapshot
from game.piece import PieceSnapshot
from game.player import Player
from game.square import Square

import pygame


Move = tuple[Square, Square]
Snapshot = tuple[list[PieceSnapshot], list[int], CapturedSnapshot, Move, str]


class History:

    def __init__(self, white: Player, black: Player, captured: Captured):
        self.pieces = white.pieces + black.pieces
        self.clocks = [white.clock, black.clock]
        self.captured = captured

        self.function_dict = {
            pygame.K_LEFT:  self.load_prev,
            pygame.K_RIGHT: self.load_next,
            pygame.K_UP:    self.load_init,
            pygame.K_DOWN:  self.load_curr
        }

    def reset(self):
        self.history: list[Snapshot] = []
        self.game_over = False
        self.save(None, None)

    def save(self, prev_move: Move, sound_effect: str):
        snapshot: Snapshot = (
            [piece.save() for piece in self.pieces],
            [clock.save() for clock in self.clocks],
            self.captured.save(),
            prev_move,
            sound_effect
        )
        self.history.append(snapshot)
        self.prev_move = prev_move
        self.index = len(self.history) - 1

    def at_current(self) -> bool:
        return self.index == len(self.history) - 1

    def load_prev(self):
        if self.index > 0:
            self.load(self.index - 1)

    def load_next(self):
        if self.index < len(self.history) - 1:
            self.load(self.index + 1)

    def load_init(self):
        if self.index > 0:
            self.load(0)

    def load_curr(self):
        if self.index < len(self.history) - 1:
            self.load(len(self.history) - 1)

    def load(self, index: int):
        (   pieces_snapshot,
            clocks_snapshot,
            captured_snapshot,
            self.prev_move,
            sound_effect
        ) = self.history[index]

        for piece, snapshot in zip(self.pieces, pieces_snapshot):
            piece.load(snapshot)

        if self.game_over:
            for clock, snapshot in zip(self.clocks, clocks_snapshot):
                clock.load(snapshot)

        self.captured.load(captured_snapshot)

        if sound_effect is not None:
            Sounds.play(sound_effect)

        self.index = index

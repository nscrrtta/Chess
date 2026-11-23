from utils.constants import SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y
from utils.common import Colours, Font, Surface, scale
import pygame


class Board:

    # For labeling files/ranks
    font = Font(28)
    x_offset = scale(4)
    y_offset = scale(3)

    def __init__(self):
        self.dark_squares: list[pygame.Rect] = []
        self.lite_squares: list[pygame.Rect] = []

        for rank in range(8):
            for file in range(8):
                rect = (
                    SQUARE_SIZE * file + BOARD_OFFSET_X,
                    SQUARE_SIZE * rank + BOARD_OFFSET_Y,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                if (file + rank) % 2 == 1:
                    self.dark_squares.append(rect)
                else:
                    self.lite_squares.append(rect)

        # Labels for each flipped position
        self.labels = {
            True:  self._get_labels(True),
            False: self._get_labels(False)
        }

    def _get_labels(self, flipped: bool) -> list[Surface]:
        labels: list[Surface] = []
        for i in range(8):
            labels.append(self._get_file_label(i, flipped))
            labels.append(self._get_rank_label(i, flipped))
        return labels

    def _get_file_label(self, val: int, flipped: bool) -> Surface:
        colour = Colours.lite_squares
        if val % 2 == 1:
            colour = Colours.dark_squares

        char = 'abcdefgh'[(7 - val) if flipped else val]

        return Surface(self.font.render(char, colour), bottomright=(
            BOARD_OFFSET_X - self.x_offset + SQUARE_SIZE * (val + 1),
            BOARD_OFFSET_Y - self.y_offset + SQUARE_SIZE * 8
        ))

    def _get_rank_label(self, val: int, flipped: bool) -> Surface:
        colour = Colours.dark_squares
        if val % 2 == 1:
            colour = Colours.lite_squares

        char = '87654321'[(7 - val) if flipped else val]

        return Surface(self.font.render(char, colour), topleft=(
            BOARD_OFFSET_X + self.x_offset,
            BOARD_OFFSET_Y + self.y_offset + SQUARE_SIZE * val
        ))

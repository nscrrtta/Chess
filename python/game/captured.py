from utils.constants import BOARD_OFFSET_X, TOP_CENTER, BOT_CENTER
from utils.common import Font, Images, Surface, int_scale
from game.piece import Piece
from game.view import View


CapturedSnapshot = tuple[dict[str, int], int]

# How far apart (in pixels) captured pieces are from their neighbours
CAPTURED_SPACING = {'p': 15, 'n': 15, 'b': 15, 'r': 15, 'q': 25}

# Material value of each piece: positive for white, negative for black
VALUES = {
    'P':  1, 'N':  3, 'B':  3, 'R':  5, 'Q':  9, 'K': 0,
    'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0,
}


class Captured:
    """Records captured pieces and the material difference between players."""

    font = Font(25, 'Arial')

    def reset(self):
        self.load(({char: 0 for char in 'PpNnBbRrQq'}, 0))

    def save(self) -> CapturedSnapshot:
        return self.count.copy(), self.difference

    def load(self, snapshot: CapturedSnapshot):
        self.count, self.difference = snapshot
        self._update()

    def add_piece(self, piece: Piece):
        self.count[piece.char] += 1
        self.difference -= VALUES[piece.char]
        self._update()

    def pawn_promoted(self, piece: Piece):
        pawn = 'P' if piece.white else 'p'
        self.difference += VALUES[piece.char] - VALUES[pawn]
        self._update_text()

    def _update(self):
        self.images: list[Surface] = []
        self.left_w = self._update_images(True)
        self.left_b = self._update_images(False)
        self._update_text()

    def _update_images(self, white: bool) -> int:
        # Start this far from left edge of screen
        left = int_scale(15) + BOARD_OFFSET_X

        # Iterate through groups of pieces
        for char, count in self.count.items():
            if white != char.isupper():
                continue

            centery = BOT_CENTER
            if white ^ View.flipped:
                centery = TOP_CENTER

            file_name = f'{'w' if white else 'b'}{char.lower()}_sm'
            image = Images.get(file_name)

            space = int_scale(CAPTURED_SPACING[char.lower()])
            for _ in range(count):
                surf = Surface(image, centery=centery, left=left)
                self.images.append(surf)
                left += space

            # Space between groups of pieces
            if count: left += int_scale(25)

        return left

    def _update_text(self):
        centery = BOT_CENTER
        if (self.difference < 0) ^ View.flipped:
            centery = TOP_CENTER

        left = self.left_b
        if self.difference < 0:
            left = self.left_w

        text = self.font.render(f'+{abs(self.difference)}')
        self.text = Surface(text, midleft=(left, centery))

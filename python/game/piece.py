from utils.constants import BOARD_OFFSET_X, BOARD_OFFSET_Y, SQUARE_SIZE
from utils.common import Images
from game.square import Square
from game.view import View


PieceSnapshot = tuple[Square, str, bool]


class Piece:

    def __init__(self, char: str):
        self.char = self.init_char = char
        self.white = char.isupper()

        self.curr_square = Square()
        self.legal_moves: set[Square] = set()

        self._set_image(char)
        self.has_moved = self.held = False

    def reset(self, square: Square):
        self.load((square, self.init_char, False))
        self.has_moved = self.held = False

    def save(self) -> PieceSnapshot:
        return self.curr_square, self.char, self.captured

    def load(self, snapshot: PieceSnapshot):
        square, char, captured = snapshot
        if self.curr_square != square:
            self.move(square, temp=True)
        if self.char != char:
            self.promote(char)
        else: self._update_xy()
        self.captured = captured

    def move(self, square: Square, temp=False):
        self.file, self.rank = square.coords()
        self.prev_square = self.curr_square
        self.curr_square = square

        if not temp:
            self._update_xy()
            self.has_moved = True

    def promote(self, char: str):
        self._set_image(char)
        self._update_xy()
        self.char = char

    def get_prev_move(self) -> tuple[Square, Square]:
        return self.curr_square, self.prev_square

    @property
    def kind(self) -> str:
        return self.char.lower()

    def is_pawn(self) -> bool:
        return self.kind == 'p'

    def is_knight(self) -> bool:
        return self.kind == 'n'

    def is_bishop(self) -> bool:
        return self.kind == 'b'

    def is_rook(self) -> bool:
        return self.kind == 'r'

    def is_queen(self) -> bool:
        return self.kind == 'q'

    def is_king(self) -> bool:
        return self.kind == 'k'

    def is_minor(self) -> bool:
        return self.is_knight() or self.is_bishop()

    def _set_image(self, char: str):
        colour = 'w' if char.isupper() else 'b'
        file_name = f'{colour}{char.lower()}_lg'

        self.image = Images.get(file_name)
        self.rect = self.image.get_rect()

    def _update_xy(self):
        file, rank = self.curr_square.coords(flip=View.flipped)
        self.rect.midbottom = (
            SQUARE_SIZE * (file + 0.50) + BOARD_OFFSET_X,
            SQUARE_SIZE * (rank + 0.93) + BOARD_OFFSET_Y
        )

from game.square import Square
from game.piece import Piece


Board = list[list[Piece | None]]


class Position:

    def reset(self):
        self.board: Board = [[None] * 8 for _ in range(8)]
        self.en_passant_square = Square()

    def get_square(self, file: int, rank: int) -> Piece | None:
        return self.board[file][rank]

    def set_square(self, file: int, rank: int, piece: Piece | None):
        self.board[file][rank] = piece

    def update_en_passant_square(self, piece: Piece):
        self.en_passant_square = Square()
        diff = abs(piece.rank - piece.prev_square.rank)
        if piece.is_pawn() and diff == 2:
            rank = piece.rank + (1 if piece.white else -1)
            self.en_passant_square = Square(piece.file, rank)

    def make_move(self, piece: Piece, square: Square, temp=False) -> Piece | None:
        if square == piece.curr_square:
            return None
        cap = self.capture_piece(piece, square)
        self.move_piece(piece, square, temp)
        return cap

    def move_piece(self, piece: Piece, square: Square, temp=False):
        if square == piece.curr_square:
            return
        self.set_square(square.file, square.rank, piece)
        self.set_square(piece.file, piece.rank, None)
        piece.move(square, temp)

    def undo_move(self, piece: Piece, cap: Piece | None):
        self.move_piece(piece, piece.prev_square, True)
        if cap is None:
            return
        self.set_square(cap.file, cap.rank, cap)
        cap.captured = False

    def capture_piece(self, piece: Piece, square: Square) -> Piece | None:
        en_passant = piece.is_pawn() and square == self.en_passant_square
        rank = piece.rank if en_passant else square.rank

        cap = self.get_square(square.file, rank)
        if cap is None:
            return None

        self.set_square(cap.file, cap.rank, None)
        cap.captured = True
        return cap

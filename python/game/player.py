from game.legal import LegalMoveCalculator
from game.position import Position
from game.square import Square
from game.clock import Clock
from game.piece import Piece


class Player:

    def __init__(self, position: Position, white: bool):
        self.position = position
        self.white = white

        # Playing pieces
        chars = 'pppppppprnbqkbnr'
        if white: chars = chars.upper()
        self.pieces = [Piece(char) for char in chars]

        self.king = self.pieces[12]

        # Pieces pawns can promote to
        chars = 'QRBN' if white else 'nbrq'
        self.promos = [Piece(char) for char in chars]

        self.clock = Clock(white)
        self.score = 0.0

    def set_opponent(self, opponent: 'Player'):
        self.opponent = opponent
        self.legal_move_calculator = LegalMoveCalculator(
            self.king, self.pieces, opponent.pieces, self.position
        )

    def reset(self, files: list[int]):
        for i, piece in enumerate(self.pieces):
            pawn_rank = 6 if piece.white else 1
            back_rank = 7 if piece.white else 0

            file = files[i % 8]
            is_pawn = piece.init_char.lower() == 'p'
            rank = pawn_rank if is_pawn else back_rank

            piece.reset(Square(file, rank))
            self.position.set_square(file, rank, piece)

    def _get_attacked_squares(self) -> set[Square]:
        return self.legal_move_calculator.get_attacked_squares()

    def calc_legal_moves(self):
        self.no_moves = not self.legal_move_calculator.calculate()

        # Determine if in check
        attacked = self._get_attacked_squares()
        self.in_check = self.king.curr_square in attacked

        # Castling
        self.can_castle_king_side = self._can_castle(attacked, True)
        self.can_castle_queen_side = self._can_castle(attacked, False)

    def castling_rights(self, king_side: bool) -> bool:
        rook = self._get_rook(king_side)
        return not (self.king.has_moved or rook.has_moved or rook.captured)

    def castle(self, king_side: bool):
        king, rook = self.king, self._get_rook(king_side)

        rank = 7 if self.white else 0
        king_file = 6 if king_side else 2
        rook_file = 5 if king_side else 3

        # Lift rook and king
        self.position.set_square(king.file, king.rank, None)
        self.position.set_square(rook.file, rook.rank, None)

        # Place rook and king
        self.position.set_square(king_file, rank, king)
        self.position.set_square(rook_file, rank, rook)

        king.move(Square(king_file, rank))
        rook.move(Square(rook_file, rank))

    def _can_castle(self, attacked: set[Square], king_side: bool) -> bool:
        # Works for standard position and Fischer Random positions

        if not self.castling_rights(king_side) or self.in_check:
            return False

        rook = self._get_rook(king_side)

        back_rank = 7 if self.white else 0
        king_file = 6 if king_side else 2
        rook_file = 5 if king_side else 3

        # Squares king/rook will move to must be empty
        for file in [king_file, rook_file]:
            other = self.position.get_square(file, back_rank)
            if other and other != self.king and other != rook:
                return False

        # No pieces between king and rook
        m = min(self.king.file, rook.file) + 1
        n = max(self.king.file, rook.file)

        for file in range(m, n):
            if self.position.get_square(file, back_rank):
                return False

        # King cannot castle through check
        m = min(self.king.file, king_file)
        n = max(self.king.file, king_file) + 1

        for file in range(m, n):
            if Square(file, back_rank) in attacked:
                return False

        return True

    def _get_rook(self, king_side: bool) -> Piece:
        return self.pieces[15 if king_side else 8]

from game.position import Position
from game.square import Square
from game.piece import Piece


# Directions each piece moves in (pawns are handled separately)
DIRECTIONS = {
    'n': [(2, 1), (-2, 1), (-2, -1), (2, -1), (1, 2), (-1, 2), (-1, -2), (1, -2)],
    'b': [(1, 1), (-1, 1), (-1, -1), (1, -1)],
    'r': [(0, 1), (-1, 0), ( 0, -1), (1,  0)],
    'q': [(0, 1), (-1, 0), ( 0, -1), (1,  0), (1, 1), (-1, 1), (-1, -1), (1, -1)],
    'k': [(0, 1), (-1, 0), ( 0, -1), (1,  0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
}


class LegalMoveCalculator:
    """Works out the legal moves for one player's pieces."""

    def __init__(self, king: Piece, my_pieces: list[Piece], their_pieces: list[Piece], position: Position):
        self.king = king
        self.my_pieces = my_pieces
        self.their_pieces = their_pieces
        self.position = position

    def calculate(self) -> bool:
        """
        Set piece.legal_moves for each of my pieces.
        Return True if at least one piece has a legal move.
        """
        has_moves = False
        for piece in self.my_pieces:
            if piece.captured:
                continue
            piece.legal_moves.clear()
            for square in self._get_squares(piece, attack=False):
                # A move is legal if it doesn't leave my king in check
                cap = self.position.make_move(piece, square, True)
                if not self._king_in_check():
                    piece.legal_moves.add(square)
                    has_moves = True
                self.position.undo_move(piece, cap)
        return has_moves

    def get_attacked_squares(self) -> set[Square]:
        """Squares attacked by the opponent's pieces."""
        squares: set[Square] = set()
        for piece in self.their_pieces:
            if not piece.captured:
                squares |= self._get_squares(piece, attack=True)
        return squares

    def _king_in_check(self) -> bool:
        return self.king.curr_square in self.get_attacked_squares()

    # Squares a piece can reach

    def _get_squares(self, piece: Piece, attack: bool) -> set[Square]:
        """
        Squares this piece can move to, ignoring whether the move leaves its king in check.
        If attack is True, return the squares it attacks instead (pawns attack diagonally only).
        """
        if piece.is_pawn():
            return self._get_squares_pawn(piece, attack)

        squares: set[Square] = set()
        distance = 7 if self._piece_slides(piece) else 1

        for d_file, d_rank in DIRECTIONS[piece.kind]:
            for i in range(1, 1 + distance):
                file = piece.file + d_file * i
                rank = piece.rank + d_rank * i

                if self._out_of_bounds(file, rank):
                    break

                # Piece located at new square
                other = self.position.get_square(file, rank)
                # Square this piece could move to
                square = Square(file, rank, other is None)

                if other is None or other.white != piece.white:
                    squares.add(square)

                if other is not None:
                    break

        return squares

    def _get_squares_pawn(self, piece: Piece, attack: bool) -> set[Square]:
        squares: set[Square] = set()
        pawn_direction = -1 if piece.white else 1

        # Diagonal moves
        for d_file in (1, -1):
            file = piece.file + d_file
            rank = piece.rank + pawn_direction

            if self._out_of_bounds(file, rank):
                continue

            # Piece located at new square
            other = self.position.get_square(file, rank)
            # Square this piece could move to
            square = Square(file, rank, other is None)

            if attack \
            or square == self.position.en_passant_square \
            or (other and other.white != piece.white):
                squares.add(square)

        if attack:
            return squares

        # Forward moves: two squares from the starting rank, otherwise one
        start_rank = 6 if piece.white else 1

        for i in range(2 if piece.rank == start_rank else 1):
            file = piece.file
            rank = piece.rank + pawn_direction * (i + 1)

            # If a piece is in the way
            if self.position.get_square(file, rank):
                break

            squares.add(Square(file, rank))

        return squares

    def _out_of_bounds(self, file: int, rank: int) -> bool:
        return file < 0 or file > 7 or rank < 0 or rank > 7

    def _piece_slides(self, piece: Piece) -> bool:
        return piece.is_bishop() or piece.is_rook() or piece.is_queen()

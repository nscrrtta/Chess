from utils.constants import SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y
from utils.common import Sounds

from game.captured import Captured
from game.position import Position
from game.flipper import Flipper
from game.history import History
from game.player import Player
from game.square import Square
from game.piece import Piece
from game.view import View

from enum import Enum
import pygame
import random


class Result(Enum):
    TIMEOUT = 1
    CHECKMATE = 2
    STALEMATE = 3
    REPETITION = 4
    FIFTY_MOVE_RULE = 5
    INSUFFICIENT_MATERIAL = 6


class Game:

    def __init__(self):
        self.position = Position()

        self.white_player = Player(self.position, True)
        self.black_player = Player(self.position, False)

        self.white_player.set_opponent(self.black_player)
        self.black_player.set_opponent(self.white_player)

        self.pieces = self.white_player.pieces \
                    + self.black_player.pieces

        self.captured = Captured()

        self.flipper = Flipper(self.white_player, self.black_player, self.captured)
        self.history = History(self.white_player, self.black_player, self.captured)

        self.new_game(True, False)

    def new_game(self, new_position: bool, fischer_random: bool):
        if new_position:
            self.fischer_files = self._get_fischer_files()

        files = range(8)
        if fischer_random:
            files = self.fischer_files

        self.position.reset()
        self.white_player.reset(files)
        self.black_player.reset(files)

        self.captured.reset()
        self.history.reset()

        self.curr_player = self.white_player
        self.curr_player.calc_legal_moves()

        self.held_piece: Piece | None = None
        self.curr_piece: Piece | None = None

        self.promo_square = Square()
        self.pawn_promoting = False

        self.half_move_counter = 0
        fen = self._get_fen_string()
        self.fen_dict = {fen: 1}

        self.result = None
        Sounds.play('gamestart')

    def _end_game(self):
        Sounds.play('gameover')
        self.history.game_over = True
        self.pawn_promoting = False
        self.curr_piece = None
        self._update_scores()

    def game_over(self) -> bool:
        return self.result is not None

    def tick_clock(self, elapsed: int):
        if self.game_over():
            return
        self.curr_player.clock.tick(elapsed)
        if self.curr_player.clock.millis <= 0:
            self.result = Result.TIMEOUT
            self._end_game()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_down(*event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse_up(*event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self._mouse_motion(*event.pos)
        elif event.type == pygame.KEYDOWN:
            self._key_down(event.key)

    def _mouse_down(self, x: int, y: int):
        square = self._xy_to_square(x, y)
        if self.pawn_promoting:
            self._promote_pawn(square)
        elif self._legal_move(square):
            self._make_move(square)
        else:
            self._select_piece(square)

    def _mouse_up(self, x: int, y: int):
        if self.pawn_promoting or self.held_piece is None:
            return

        self._drop_held_piece()
        if self.curr_piece is None:
            return

        side = self._castling_side(x, y)
        if side is not None:
            self._castle(side)
            return

        square = self._xy_to_square(x, y)
        if self._legal_move(square):
            self._make_move(square)

    def _mouse_motion(self, x: int, y: int):
        if self.held_piece is not None:
            self.held_piece.rect.center = (x, y)

    def _key_down(self, key: int):
        if key == pygame.K_f:
            self.flipper.flip()
        elif key in self.history.function_dict:
            if self.held_piece is None and not self.pawn_promoting:
                self.history.function_dict[key]()

    def _select_piece(self, square: Square):
        self.curr_piece = None

        for piece in self.pieces:
            if piece.captured:
                continue
            if piece.curr_square == square:
                self._pick_up_piece(piece)
                break
        else: return

        if self.game_over():
            return
        if not self.history.at_current():
            return
        if piece.white != self.curr_player.white:
            return
        self.curr_piece = piece

    def _pick_up_piece(self, piece: Piece):
        self.held_piece = piece
        piece.held = True

    def _drop_held_piece(self):
        if self.held_piece is not None:
            self.held_piece._update_xy()
            self.held_piece.held = False
            self.held_piece = None

    def _castle(self, king_side: bool):
        self.position.en_passant_square = Square()
        self.curr_player.castle(king_side)
        self.half_move_counter += 1
        self._next_turn('castle')

    def _promote_pawn(self, square: Square):
        for piece in self.curr_player.promos:
            if piece.curr_square == square:
                break
        else: return

        self.curr_piece.promote(piece.char)
        self._make_move(self.promo_square)

    def _legal_move(self, square: Square) -> bool:
        if self.curr_piece is None:
            return False
        return square in self.curr_piece.legal_moves

    def _make_move(self, square: Square):
        if self.curr_piece.is_pawn() and square.rank % 7 == 0:
            self._move_promotions(square)
            return

        cap = self.position.make_move(self.curr_piece, square)
        self.position.update_en_passant_square(self.curr_piece)

        self.half_move_counter += 1
        sound = 'move'

        if self.curr_piece.is_pawn():
            self.half_move_counter = 0

        if cap is not None:
            self.half_move_counter = 0
            self.captured.add_piece(cap)
            sound = 'capture'

        if self.pawn_promoting:
            self.half_move_counter = 0
            self.captured.pawn_promoted(self.curr_piece)
            self.pawn_promoting = False
            sound = 'promote'

        self._next_turn(sound)

    def _next_turn(self, sound_effect: str):
        self.curr_player.clock.stop()

        self.curr_player = self.curr_player.opponent
        self.curr_player.calc_legal_moves()

        if self.curr_player.in_check:
            sound_effect = 'check'
        Sounds.play(sound_effect)

        fen = self._get_fen_string()
        count = self.fen_dict.get(fen, 0) + 1
        self.fen_dict[fen] = count

        if self.curr_player.no_moves:
            self.result = Result.STALEMATE
            if self.curr_player.in_check:
                self.result = Result.CHECKMATE
        elif count >= 3:
            self.result = Result.REPETITION
        elif self.half_move_counter >= 100:
            self.result = Result.FIFTY_MOVE_RULE
        elif self._insufficient_material():
            self.result = Result.INSUFFICIENT_MATERIAL

        prev_move = self.curr_piece.get_prev_move()
        self.history.save(prev_move, sound_effect)
        self.curr_piece = None

        if self.game_over():
            self._end_game()

    def _move_promotions(self, square: Square):
        self.promo_square = square
        self.pawn_promoting = True

        # Pawn is either located on rank 0 or rank 7
        #
        # If pawn is at rank 0 (top of board)
        # pieces are moved to ranks 0 -> 3
        #
        # If pawn is at rank 7 (bottom of board)
        # pieces are moved to ranks 4 -> 7
        file, rank = square.coords()
        rank = 0 if rank < 4 else 4

        for i, piece in enumerate(self.curr_player.promos):
            piece.move(Square(file, rank + i))

    def _update_scores(self):
        if self.result == Result.TIMEOUT \
        or self.result == Result.CHECKMATE:
            self.curr_player.opponent.score += 1.0
        else:
            self.white_player.score += 0.5
            self.black_player.score += 0.5

    def _insufficient_material(self) -> bool:
        num_minor_pieces = 0

        white_bishop: Piece | None = None
        black_bishop: Piece | None = None

        for piece in self.pieces:
            if piece.captured or piece.is_king():
                continue
            if not piece.is_minor():
                return False
            num_minor_pieces += 1
            if not piece.is_bishop():
                continue
            if piece.white:
                if white_bishop is not None:
                    return False
                white_bishop = piece
            else:
                if black_bishop is not None:
                    return False
                black_bishop = piece

        # K+B vs K+B, bishops on same-coloured squares
        if num_minor_pieces == 2 and white_bishop and black_bishop:
            a = white_bishop.curr_square.is_light_square()
            b = black_bishop.curr_square.is_light_square()
            return a == b

        # K vs K, K+N vs K or K+B vs K
        return num_minor_pieces < 2

    def _castling_side(self, x: int, y: int) -> bool | None:
        """
        Return True if castling king side, or False if castling queen side.

        Return None if player is unable to castle, or they did not drag
        their king far enough in the direction they are trying to castle.
        """
        player = self.curr_player
        king = player.king

        if self.curr_piece != king or self._xy_to_square(x, y).rank != king.rank:
            return None

        # King must be dragged at least two squares left or right on screen
        col = 7 - king.file if View.flipped else king.file
        left = x < SQUARE_SIZE * (col - 1) + BOARD_OFFSET_X
        right = x > SQUARE_SIZE * (col + 2) + BOARD_OFFSET_X

        # King not dragged far enough left or right
        if not (left or right):
            return None

        # Side player is trying to castle to depends on if game is flipped.
        # Dragging right -> Queen side if game flipped, else king side.
        # Dragging left -> King side if game flipped, else queen side.
        king_side = View.flipped if left else not View.flipped

        if king_side and not player.can_castle_king_side:
            return None
        if not king_side and not player.can_castle_queen_side:
            return None
        return king_side

    def _xy_to_square(self, x: int, y: int) -> Square:
        """Board square under pixel (x, y)."""
        file = int((x - BOARD_OFFSET_X) // SQUARE_SIZE)
        rank = int((y - BOARD_OFFSET_Y) // SQUARE_SIZE)
        if View.flipped:
            file = 7 - file
            rank = 7 - rank
        return Square(file, rank)

    def _get_fen_string(self) -> str:
        fen = []

        # Pieces
        rows = []
        for rank in range(8):
            empty, row = 0, ''
            for file in range(8):
                piece = self.position.get_square(file, rank)
                if piece is None:
                    empty += 1
                else:
                    if empty:
                        row += str(empty)
                    row += piece.char
                    empty = 0
            if empty:
                row += str(empty)
            rows.append(row)
        pieces = '/'.join(rows)

        # Colour of active player
        active_colour = 'w' if self.curr_player.white else 'b'

        # Castling privileges
        castling = ''
        for player in [self.white_player, self.black_player]:
            if player.castling_rights(True):
                castling += ('K' if player.white else 'k')
            if player.castling_rights(False):
                castling += ('Q' if player.white else 'q')

        # En passant square
        en_passant = str(self.position.en_passant_square)

        return ' '.join([pieces, active_colour, castling, en_passant])

    def _get_fischer_files(self) -> list[int]:

        def pick_and_remove(condition) -> int:
            options = [f for f in empty_files if condition(f)]
            choice = random.choice(options)
            empty_files.remove(choice)
            return choice

        files = [0] * 8
        empty_files = list(range(8))

        # King must be placed such that a rook can be on either side
        files[4] = pick_and_remove(lambda f: 0 < f < 7)

        # King-side rook must be to the right of the king
        files[7] = pick_and_remove(lambda f: f > files[4])

        # Queen-side rook must be to the left of the king
        files[0] = pick_and_remove(lambda f: f < files[4])

        # Bishops must be on opposite-colored squares
        files[2] = pick_and_remove(lambda f: f % 2 == 0)
        files[5] = pick_and_remove(lambda f: f % 2 == 1)

        # Knights can go on any remaining squares
        files[1] = pick_and_remove(lambda _: True)
        files[6] = pick_and_remove(lambda _: True)

        # One square left for queen
        files[3] = empty_files[0]

        return files

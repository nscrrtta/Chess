from utils.constants import SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y
from utils.common import Colours, int_scale

from game.square import Square
from game.board import Board
from game.clock import Clock
from game.piece import Piece
from game.game import Game
from game.view import View

import pygame


class Renderer:

    def __init__(self, window: pygame.Surface, game: Game):
        self.window = window
        self.game = game

        self.board = Board()

        # Surface for drawing transparent shapes
        self.surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.surf.set_alpha(100)

    def draw(self):
        self.window.fill(Colours.grey(50))
        self._draw_board()
        self._draw_transparent()
        self._draw_pieces()
        self._draw_promotions()
        self._draw_captured()
        self._draw_clock(self.game.curr_player.clock, False)
        self._draw_clock(self.game.curr_player.opponent.clock, True)
        self._draw_held_piece()

    def _draw_board(self):
        for rect in self.board.dark_squares:
            pygame.draw.rect(self.window, Colours.dark_squares, rect)
        for rect in self.board.lite_squares:
            pygame.draw.rect(self.window, Colours.lite_squares, rect)
        for label in self.board.labels[View.flipped]:
            self.window.blit(label.surf, label.rect)

    def _draw_transparent(self):
        highlights:  set[Square] = set()
        legal_moves: set[Square] = set()

        if self.game.history.prev_move:
            for square in self.game.history.prev_move:
                highlights.add(square)

        piece = self.game.curr_piece
        if piece and not self.game.pawn_promoting:
            highlights.add(piece.curr_square)
            legal_moves = piece.legal_moves

        for square in highlights:
            self._transparent_square(square)

        for square in legal_moves:
            self._transparent_circle(square)

    def _draw_pieces(self):
        for piece in self.game.pieces:
            if piece.captured or piece.held:
                continue
            if piece == self.game.curr_piece \
            and self.game.pawn_promoting:
                continue
            self._draw_piece(piece)

    def _draw_piece(self, piece: Piece):
        self.window.blit(piece.image, piece.rect)

    def _draw_captured(self):
        captured = self.game.captured
        for image in captured.images:
            self.window.blit(image.surf, image.rect)
        if captured.difference != 0:
            self.window.blit(captured.text.surf, captured.text.rect)

    def _draw_clock(self, clock: Clock, transparent: bool):
        pygame.draw.rect(self.window, clock.rect_colour, clock.rect, 0, clock.radius)
        self.window.blit(clock.text.surf, clock.text.rect)

        transparent |= (self.game.game_over() or not clock.in_use)
        surf = clock.transparent if transparent else clock.image
        self.window.blit(surf.surf, surf.rect)

    def _draw_promotions(self):
        if not self.game.pawn_promoting:
            return

        promos = self.game.curr_player.promos
        square = self.game.promo_square

        file, rank = square.coords(flip=View.flipped)
        rank = 0 if rank < 4 else 4

        rect = pygame.Rect(
            SQUARE_SIZE * file + BOARD_OFFSET_X,
            SQUARE_SIZE * rank + BOARD_OFFSET_Y,
            SQUARE_SIZE * 1,
            SQUARE_SIZE * len(promos)
        )

        radius = int_scale(10)
        pygame.draw.rect(self.window, Colours.grey(200), rect, 0, radius)
        pygame.draw.rect(self.window, Colours.black, rect, 1, radius)

        for piece in promos:
            self._draw_piece(piece)

    def _draw_held_piece(self):
        if self.game.held_piece is not None:
            self._draw_piece(self.game.held_piece)

    def _transparent_square(self, square: Square):
        rect = pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE)

        self.surf.fill((*Colours.black, 0))
        colour = Colours.highlight

        pygame.draw.rect(self.surf, colour, rect)
        self.window.blit(self.surf, self._square_topleft(square))

    def _transparent_circle(self, square: Square):
        radius = int_scale(12 if square.empty else 45)
        width  = int_scale( 0 if square.empty else  8)
        x = y = SQUARE_SIZE // 2

        self.surf.fill((*Colours.black, 0))
        colour = Colours.grey(90)

        pygame.draw.circle(self.surf, colour, (x, y), radius, width)
        self.window.blit(self.surf, self._square_topleft(square))

    def _square_topleft(self, square: Square) -> tuple[float, float]:
        file, rank = square.coords(flip=View.flipped)
        return (
            SQUARE_SIZE * file + BOARD_OFFSET_X,
            SQUARE_SIZE * rank + BOARD_OFFSET_Y
        )

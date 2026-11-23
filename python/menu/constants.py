from utils.common import scale_point
from game.game import Result


#
# Center positions of components in menu,
# measured from the top-left corner of the window
#

# Game result and score
MENU_LARGE_TEXT = scale_point(370, 195)
MENU_SMALL_TEXT = scale_point(370, 250)
MENU_SCORE_TEXT = scale_point(370, 310)

# Pawns beside the score and the clock inputs
MENU_WHITE_PAWN_LG = scale_point(255, 310)
MENU_BLACK_PAWN_LG = scale_point(470, 310)
MENU_WHITE_PAWN_SM = scale_point(210, 385)
MENU_BLACK_PAWN_SM = scale_point(210, 445)

# Clock inputs: minutes, ':', seconds, '+', increment
MENU_WHITE_CLOCK = [scale_point(x, 385) for x in (270, 320, 370, 420, 470)]
MENU_BLACK_CLOCK = [scale_point(x, 445) for x in (270, 320, 370, 420, 470)]

# Buttons
MENU_NEW_GAME     = scale_point(370, 520)
MENU_CHECKBOX     = scale_point(255, 583)
MENU_FRAND_TEXT   = scale_point(390, 583)
MENU_NEW_POSITION = scale_point(370, 640)

# Large and small text shown for each game result.
# {colour} is filled in with 'White' or 'Black'.
MENU_RESULT_TEXT = {
    # Game in progress
    None: ('', ''),

    # Decisive results
    Result.TIMEOUT: ('{colour} Wins!', 'By Timeout'),
    Result.CHECKMATE: ('{colour} Wins!', 'By Checkmate'),

    # Draws
    Result.STALEMATE: ('Draw!', 'By Stalemate'),
    Result.REPETITION: ('Draw!', 'By Repetition'),
    Result.FIFTY_MOVE_RULE: ('Draw!', 'By Fifty Move Rule'),
    Result.INSUFFICIENT_MATERIAL: ('Draw!', 'By Insufficient Material'),
}

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

IMAGES_DIR = ROOT_DIR / 'pngs'
SOUNDS_DIR = ROOT_DIR / 'wavs'

FPS = 60

# Everything scales according to this value
SCALE = 1.0

SQUARE_SIZE = 90 * SCALE

BOARD_OFFSET_X = 10 * SCALE
# Space where captured pieces and clocks are drawn
BOARD_OFFSET_Y = 60 * SCALE

# Window:
#################
#      GAP      #
#################
#               #
#               #
#  CHESS BOARD  #
#               #
#               #
#################
#      GAP      #
#################

WINDOW_WIDTH  = SQUARE_SIZE * 8 + BOARD_OFFSET_X * 2
WINDOW_HEIGHT = SQUARE_SIZE * 8 + BOARD_OFFSET_Y * 2

TOP_CENTER = BOARD_OFFSET_Y / 2
BOT_CENTER = WINDOW_HEIGHT - BOARD_OFFSET_Y / 2

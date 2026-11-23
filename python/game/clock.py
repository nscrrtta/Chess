from utils.constants import WINDOW_WIDTH, BOARD_OFFSET_X, TOP_CENTER, BOT_CENTER
from utils.common import Colours, Font, Images, Surface, scale, int_scale
from game.view import View
import pygame


class Clock:

    # Rect dimensions
    radius = int_scale(8)
    width  = scale(175)
    height = scale(40)

    right_edge = WINDOW_WIDTH - BOARD_OFFSET_X - scale(10)
    left_edge = right_edge - width

    font = Font(25, 'Arial')

    def __init__(self, white: bool):
        self.white = white

        if white:
            self.font_colour = Colours.grey(30)
            self.rect_colour = Colours.white
        else:
            self.font_colour = Colours.white
            self.rect_colour = Colours.grey(30)

        self._load_transparent_surface()
        self._load_image()
        self._load_rect()

        self.reset()

    def reset(self, seconds=0, increment=0):
        """
        seconds = 0 means the clock isn't used
        (shows 10:00 and never ticks).
        """
        self.in_use = seconds > 0

        if seconds == 0:
            seconds = 600

        self.increment = increment
        self.load(seconds * 1000)

    def save(self) -> int:
        return self.millis

    def load(self, millis: int):
        self.millis = millis
        self._update_text()

    def stop(self):
        if not self.in_use:
            return
        if self.increment > 0:
            self.millis += self.increment * 1000
            self._update_text()

    def tick(self, elapsed: int):
        """Subtract elapsed milliseconds of real time (never going below 0)."""
        if not self.in_use or elapsed <= 0:
            return
        prev_millis = self.millis
        self.millis = max(0, self.millis - elapsed)
        self._update_text()

        # Rotate the icon once when the clock passes a whole second
        if (prev_millis - 1) // 1000 != (self.millis - 1) // 1000:
            self.image.rotate()

    def _update_text(self):
        seconds, millis = divmod(self.millis, 1000)
        minutes, seconds = divmod(seconds, 60)

        colour = Colours.grey(30) if self.white else Colours.white

        if self.millis < 10_000:
            l, r = seconds, millis // 10
            colour = Colours.red
        elif minutes > 0:
            l, r = minutes, seconds
        else: l, r = 0, seconds

        self.text = Surface(
            self.font.render(f'{l}:{r:02d}', colour),
            midright=(self.right_edge - 10, self._get_centery())
        )

    def _load_transparent_surface(self):
        # Transparent grey rectangle - drawn when clock is inactive
        self.transparent = Surface(
            pygame.Surface((self.width, self.height), pygame.SRCALPHA),
            midleft=(self.left_edge, self._get_centery())
        )
        pygame.draw.rect(
            self.transparent.surf, (*Colours.grey(125), 127),
            (0, 0, self.width, self.height), 0, self.radius
        )

    def _load_image(self):
        file_name = f'clock_{'white' if self.white else 'black'}'
        self.image = Surface(Images.get(file_name), midleft=(
            self.left_edge + scale(12), self._get_centery()
        ))

    def _load_rect(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midleft = (self.left_edge, self._get_centery())

    def _get_centery(self) -> float:
        if self.white ^ View.flipped:
            return BOT_CENTER
        return TOP_CENTER

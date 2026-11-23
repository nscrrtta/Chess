from utils.common import Font, Point, Surface, scale
from menu.rect import ClickableRect


class NumberInput(ClickableRect):

    font = Font(45)

    def __init__(self, center: Point, z_fill=False):
        super().__init__(center, width=64, height=48)
        self.z_fill = z_fill

        # Numeric value (0-59)
        self.value = 0

        # Number of digits shown (0-2). Leading zeros count
        self.num_digits = 0

        self._update_text()

    def input_number(self, n: int):
        value = self.value * 10 + n
        if self.num_digits < 2 and value < 60:
            self.value = value
            self.num_digits += 1
            self._update_text()

    def remove_number(self):
        """Remove the last digit."""
        if self.num_digits > 0:
            self.value //= 10
            self.num_digits -= 1
            self._update_text()

    def leave_focus(self):
        self.pressed = False
        if self.z_fill and self.num_digits == 1:
            self.num_digits = 2
            self._update_text()

    def _update_text(self):
        """Re-render the displayed number."""
        string = f'{self.value:0{self.num_digits}}' if self.num_digits else ''
        midright = self.rect.right - scale(10), self.rect.centery + scale(2)
        self.text = Surface(self.font.render(string), midright=midright)

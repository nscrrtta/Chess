from utils.common import Font, Point, Surface, scale
from menu.rect import ClickableRect


class Button(ClickableRect):

    font = Font(45)

    # A button is drawn with two rects to create a 3D appearance.
    # Top rect moves down <dy> pixels when the button is pressed.
    dy = scale(3)

    def __init__(self, center: Point, width=350, height=60, text=''):
        # self.rect is the top rect; the bottom rect sits below it
        super().__init__(center, width, height)
        self.bot_rect = self.rect.move(0, scale(7))

        # Label, centered in the top rect
        self.text = Surface(self.font.render(text), center=center)

        # Can only click button when enabled.
        # Button is grey when disabled.
        self.enabled = True

    def press(self):
        if not self.pressed:
            self.text.rect.top += self.dy
            self.rect.top += self.dy
            self.pressed = True

    def depress(self):
        if self.pressed:
            self.text.rect.centery = self.y
            self.rect.centery = self.y
            self.pressed = False

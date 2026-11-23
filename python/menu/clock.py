from utils.common import Font, Point, Surface
from menu.number import NumberInput


class ClockInput:
    """
    A row of three number inputs.
    (Left to right): Minutes, seconds, increment.
    Renders text between each input (':' and '+').
    """

    font = Font(45)

    def __init__(self, centers: list[Point]):
        minute, colon, second, plus, increment = centers

        self.inputs = [
            NumberInput(minute),
            NumberInput(second, z_fill=True),
            NumberInput(increment)
        ]

        # ':' and '+' drawn between the inputs
        self.text = [
            Surface(self.font.render(':'), center=colon),
            Surface(self.font.render('+'), center=plus)
        ]

    def get_seconds(self) -> int:
        # minutes * 60 + seconds
        return self.inputs[0].value * 60 + self.inputs[1].value

    def get_increment(self) -> int:
        return self.inputs[2].value

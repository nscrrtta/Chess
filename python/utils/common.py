from utils.constants import SCALE, IMAGES_DIR, SOUNDS_DIR
import pygame


Point = tuple[float, float]
Colour = tuple[int, int, int]


def scale(n: int) -> float:
    return SCALE * n

def int_scale(n: int) -> int:
    return int(scale(n))

def scale_point(x: int, y: int) -> Point:
    return scale(x), scale(y)


class Colours:

    @staticmethod
    def grey(i: int) -> Colour:
        return (i, i, i)

    white = grey(255)
    black = grey(0)

    red = (255, 0, 0)

    dark_squares = (118, 150, 86)
    lite_squares = (238, 238, 210)

    button_top = (118, 150, 86)
    button_bot = (58, 90, 26)

    highlight = (255, 219, 28)


class Font:

    def __init__(self, size: int, font=None):
        self.font = pygame.font.SysFont(font, int_scale(size))

    def render(self, text: str, colour: Colour = Colours.white) -> pygame.Surface:
        return self.font.render(text, True, colour)


class Surface:

    def __init__(self, surf: pygame.Surface, **kwargs):
        self.rect = surf.get_rect(**kwargs)
        self.surf = surf

    def rotate(self):
        self.surf = pygame.transform.rotate(self.surf, -90)


class Images:

    _images: dict[str, pygame.Surface] = {}

    @classmethod
    def get(cls, file_name: str) -> pygame.Surface:
        if not cls._images:
            for file_path in IMAGES_DIR.iterdir():
                if file_path.name.endswith('.png'):
                    image = pygame.image.load(file_path)
                    cls._images[file_path.stem] = pygame.transform.smoothscale_by(image, SCALE)
        return cls._images[file_name]


class Sounds:

    _sounds: dict[str, pygame.mixer.Sound] = {}

    @classmethod
    def play(cls, file_name: str):
        if not cls._sounds:
            pygame.mixer.init()
            for file_path in SOUNDS_DIR.iterdir():
                if file_path.name.endswith('.wav'):
                    cls._sounds[file_path.stem] = pygame.mixer.Sound(file_path)
        cls._sounds[file_name].play()

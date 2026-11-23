from utils.common import Point, scale
import pygame


class ClickableRect:

    def __init__(self, center: Point, width: float, height: float):
        self.x, self.y = center
        width, height = scale(width), scale(height)
        left, top = self.x - width / 2, self.y - height / 2
        self.rect = pygame.Rect(left, top, width, height)
        self.pressed = False

    def clicked(self, x: int, y: int) -> bool:
        return self.rect.collidepoint(x, y)

import pygame

from vec2d import Vec2d
from color import Color

class Wall:

    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        self.position = Vec2d((self.pos1.x + self.pos2.x)/2, (self.pos1.y + self.pos2.y)/2)

        print(self.position)
        self.color = Color.WHITE

    def draw(self, target):
        pygame.draw.line(target, self.color, (self.pos1.x, self.pos1.y), (self.pos2.x, self.pos2.y))
    
    def update(self):
        pass

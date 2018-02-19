import pygame
import math

from vec2d import Vec2d
from color import Color

class Bullet(pygame.sprite.Sprite):

    COUNT = 0

    def __init__(self, color, angle, pos, target):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.speed = 5
        self.rot = angle
        self.pos = pos
        self.move_vec = self.rotate_point_around_pivot(
            Vec2d(0 , self.speed), Vec2d(0, 0), angle)
        self.image = pygame.Surface([3,3])
        self.image.fill(color)
        self.target = target

    def update(self):
        self.pos = self.pos - self.move_vec
    
    def draw(self):
        self.target.blit(self.image, [self.pos.x, self.pos.y])
    
    def rotate_point_around_pivot(self, point, pivot, angle):
        newPoint = point.copy()
        rad = angle * (math.pi / 180)
        s = math.sin(rad)
        c = math.cos(rad)

        # translate point back to origin:
        newPoint.x -= pivot.x
        newPoint.y -= pivot.y
        
        # rotate point
        xnew = newPoint.x * c - newPoint.y * s
        ynew = newPoint.x * s + newPoint.y * c
        
        # translate point back:
        newPoint.x = xnew + pivot.x
        newPoint.y = ynew + pivot.y
        return newPoint
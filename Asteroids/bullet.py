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
        self.image = pygame.Surface([4,4])
        self.image.fill(color)
        self.radius = 2
        self.rect = self.image.get_rect()
        self.target = target
       

    def update(self, target):
        self.pos = self.pos - self.move_vec

        if self.pos.x < 0 or self.pos.x > target.get_width() or self.pos.y < 0 or self.pos.y > target.get_height():
                Bullet.COUNT = Bullet.COUNT - 1
                self.kill()
        else:   
            self.rect.x = self.pos.x - self.radius
            self.rect.y = self.pos.y - self.radius

    def collisions(self, target_group):
        
        hits = pygame.sprite.spritecollide(self, target_group, False, pygame.sprite.collide_circle)
        if hits:
            Bullet.COUNT = Bullet.COUNT - 1
            self.kill()
            return hits
        else:
            return False
            
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
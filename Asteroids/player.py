import pygame
import math

from color import Color
from vec2d import Vec2d
from bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, color, rad, target, pos=None):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.target = target
        self.min_x = 25
        self.min_y = 25
        self.max_x = target.get_width()
        self.max_y = target.get_height()
        self.move_vec = Vec2d(0, 0)

        # dimensions
        self.rad = rad
        self.width = self.rad + self.rad
        self.height = self.rad + self.rad
        self.color = color

        # movement variables
        self.speed = 0
        self.accel = 0.01
        self.max_speed = 10
        self.rotation = 0
        
        # position variables
        self.pos = pos if pos else Vec2d(0, 0)
        self.local_pos = Vec2d(self.rad, self.rad)
        self.global_pos = Vec2d(self.pos.x - self.rad,
                            self.pos.y - self.rad)

        # player draw points
        self.p1 = Vec2d(self.width // 2, 0)
        self.p2 = Vec2d(5, self.height - 5)
        self.p3 = Vec2d(self.width - 5, self.height - 5)

        self.draw_self()

    def draw_self(self):
        # Addition is cheaper than multiplication
        try:
            self.image.fill(Color.BLACK)
        except:
            self.image = pygame.Surface(
                [
                    self.rad + self.rad, 
                    self.rad + self.rad
                ])

        new_p1 = self.rotate_point_around_pivot(self.p1, self.local_pos, self.rotation)
        new_p2 = self.rotate_point_around_pivot(self.p2, self.local_pos, self.rotation)
        new_p3 = self.rotate_point_around_pivot(self.p3, self.local_pos, self.rotation)

        pygame.draw.circle(self.image, self.color,
                        [self.local_pos.x, self.local_pos.y],
                        self.rad, 1)
        pygame.draw.line(self.image, self.color,
                        [new_p1.x, new_p1.y],
                        [new_p2.x, new_p2.y])
        pygame.draw.line(self.image, self.color,
                        [new_p1.x, new_p1.y],
                        [new_p3.x, new_p3.y])
        pygame.draw.line(self.image, self.color,
                        [new_p2.x, new_p2.y],
                        [new_p3.x, new_p3.y])

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
    
    def update(self):
        k = pygame.key.get_pressed()

        if k[pygame.K_UP]:
            self.speed = self.speed + self.accel
        if k[pygame.K_LEFT]:
            self.rotation = self.rotation - 5
        if k[pygame.K_DOWN]:
            self.speed = self.speed - self.accel
        if k[pygame.K_RIGHT]:
           self.rotation = self.rotation + 5

        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < 0:
            self.speed = 0
        
        self.__change_pos()
        self.draw_self()

    def get_real_pos(self):
        return Vec2d(self.global_pos.x + self.local_pos.x, self.global_pos.y + self.local_pos.y)

    def __change_pos(self):
        mov_vec = self.rotate_point_around_pivot(
            Vec2d(0, 0 - self.speed),
            Vec2d(0, 0), self.rotation) 
        
        self.global_pos.x = self.global_pos.x + mov_vec.x
        self.global_pos.y = self.global_pos.y + mov_vec.y

        # wrap player
        real_pos = self.get_real_pos()

        if real_pos.x > self.max_x:
            self.global_pos.x = self.min_x + self.local_pos.x
        elif real_pos.x < self.min_x:
            self.global_pos.x = self.max_x - self.local_pos.x
        
        if real_pos.y > self.max_y:
            self.global_pos.y = self.min_y + self.local_pos.y
        elif real_pos.y < self.min_y:
            self.global_pos.y = self.max_y - self.local_pos.y

    def draw(self):
        self.target.blit(self.image, [self.global_pos.x, self.global_pos.y])

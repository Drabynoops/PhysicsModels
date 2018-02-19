import pygame
import math

from color import Color
from vec2d import Vec2d
from bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, color, radius, target, pos=None):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.target = target
        self.min_x = 25
        self.min_y = 25
        self.max_x = target.get_width()
        self.max_y = target.get_height()
        self.mov_vec = Vec2d(0, 0)

        # dimensions
        self.radius = radius
        self.width = self.radius + self.radius
        self.height = self.radius + self.radius
        self.color = color

        # movement variables
        self.speed = 0
        self.accel = 0.001
        self.max_speed = 3
        self.rotation = 0
        
        # position variables
        self.pos = pos if pos else Vec2d(0, 0)
        self.local_pos = Vec2d(self.radius, self.radius)
        self.global_pos = Vec2d(self.pos.x - self.radius,
                            self.pos.y - self.radius)                         

        # player draw points
        self.p1 = Vec2d(self.width // 2, 0)
        self.p2 = Vec2d(5, self.height - 5)
        self.p3 = Vec2d(self.width - 5, self.height - 5)

        self.draw_self()
        # collision
        self.rect = self.image.get_rect()   

    def draw_self(self):
        # Addition is cheaper than multiplication
        try:
            self.image.fill(Color.BLACK)
        except:
            self.image = pygame.Surface(
                [
                    self.radius + self.radius, 
                    self.radius + self.radius
                ])

        new_p1 = self.rotate_point_around_pivot(self.p1, self.local_pos, self.rotation)
        new_p2 = self.rotate_point_around_pivot(self.p2, self.local_pos, self.rotation)
        new_p3 = self.rotate_point_around_pivot(self.p3, self.local_pos, self.rotation)

        pygame.draw.circle(self.image, self.color,
                        [self.local_pos.x, self.local_pos.y],
                        self.radius, 1)
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
        radius = angle * (math.pi / 180)
        s = math.sin(radius)
        c = math.cos(radius)

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

        if k[pygame.K_RIGHT]:
           self.rotation = self.rotation + 5
           self.speed = 0
        if k[pygame.K_LEFT]:
            self.rotation = self.rotation - 5
            self.speed = 0
        if k[pygame.K_UP]:
            self.speed = self.speed + self.accel
        if k[pygame.K_DOWN]:
            self.speed = self.speed - self.accel

        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < 0:
            self.speed = 0
        
        self.__change_pos()
        self.draw_self()

    def get_real_pos(self):
        return Vec2d(self.global_pos.x + self.local_pos.x, self.global_pos.y + self.local_pos.y)

    def __change_pos(self):
        new_mov_vec = self.rotate_point_around_pivot(
            Vec2d(0, 0 - self.speed),
            Vec2d(0, 0), self.rotation) 
        
        if (self.mov_vec + new_mov_vec).get_length() <= self.max_speed:
            self.mov_vec = self.mov_vec + new_mov_vec

        self.global_pos.x = self.global_pos.x + self.mov_vec.x
        self.global_pos.y = self.global_pos.y + self.mov_vec.y

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
        
        self.rect.x = self.global_pos.x - self.radius
        self.rect.y = self.global_pos.y - self.radius

    def draw(self):
        self.target.blit(self.image, [self.global_pos.x, self.global_pos.y])
    
    def collision(self, target_group):
        hits = pygame.sprite.spritecollide(self, target_group, False, pygame.sprite.collide_circle)
        if hits:
            return True
        else:
            return False
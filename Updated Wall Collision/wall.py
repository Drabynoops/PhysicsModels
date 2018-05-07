# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 15:52:54 2018

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d
from KinematicObject import KinematicObject

class Wall(KinematicObject):
    def __init__(self, pos, normal, color, e=0, mu=0):
        # pos, vel, density, points, color, e=0, mu=0, angle=0, angvel=0
        super().__init__(pos, Vec2d(0,0), 1, [Vec2d(0,0)], color, e, mu)
        self.normals = [normal.normalized()] # makes a copy automatically
        self.mass = 1e99
        self.moment = 1e99
        self.type = "wall"
        self.e = e
        self.mu = mu

    def calculate_area(self):
        return 1e99
      
    def check_collision(self, other, result=[]):
      if other.type == "polygon" or other.type == "kinematic":
        result.extend([self, other, 1e99, None, None])
        return True
      else:
        return False
    
    def draw(self, screen, coords):
        pos = coords.pos_to_screen(self.pos)
        normal = coords.unitvec_to_other(self.normals[0])
        X = screen.get_width()-1
        Y = screen.get_height()-1
        perp = normal.perpendicular()
        if perp.x == 0:
            start = Vec2d(pos.x, 0)
            end   = Vec2d(pos.x, Y)
        elif perp.y == 0:
            start = Vec2d(0, pos.y)
            end   = Vec2d(X, pos.y)
        else:
            s = []
            s.append((0-pos.x)/perp.x)                
            s.append((0-pos.y)/perp.y)                
            s.append((X-pos.x)/perp.x)                
            s.append((Y-pos.y)/perp.y)
            s.sort()
            start = pos + perp*s[1]
            end   = pos + perp*s[2]
        pygame.draw.line(screen, self.color, start, end, 1)        
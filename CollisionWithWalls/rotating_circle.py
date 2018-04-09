# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:38:47 2018

@author: Student
"""
import pygame
import math
from circle import Circle
from vec2d import Vec2d
from color import Color

class RotatingCircle(Circle):
    def __init__(self, pos, vel, mass, radius, color, linecolor, angle=0, angvel=0):
        super().__init__(pos, vel, mass, radius, color)
        self.angle = angle
        self.linecolor = linecolor
        self.inertia = 0.5 * self.mass * self.radius * self.radius
    
    def draw(self, target, coords):
        super().draw(target, coords)
        endpoint = self.pos + Vec2d(self.radius * math.cos(self.angle), self.radius * math.sin(self.angle))
        pygame.draw.line(target, self.linecolor, coords.pos_to_screen(self.pos).int(), 
                         coords.pos_to_screen(endpoint).int())
        
        
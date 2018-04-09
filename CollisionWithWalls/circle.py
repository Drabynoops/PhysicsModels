# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d

class Circle:
    def __init__(self, pos, vel, mass, radius, color):
        self.id = 0
        self.pos = pos.copy()
        self.mass = mass
        self.radius = radius
        self.vel = vel.copy()
        self.mom = self.vel*self.mass
        self.color = color
        self.force = Vec2d(0,0)
        self.type = "circle"
    
    def update_mom(self, dt):
        self.mom += self.force*dt
        self.update_vel()
        
    def set_vel(self, vel):
        self.vel.copy_in(vel)
        self.mom.copy_in(self.vel*self.mass)

    def update_vel(self):
        self.vel.copy_in(self.mom/self.mass)

    def update_pos(self, dt):
        self.pos += self.vel*dt

    def update(self, dt):
        self.update_mom(dt)
        self.update_pos(dt)
                
    def draw(self, screen, coords):
        #print("radius", self.radius, coords.scalar_to_screen(self.radius))
        pygame.draw.circle(screen, self.color, 
                           coords.pos_to_screen(self.pos).int(), 
                           int(coords.scalar_to_screen(self.radius)+0.5), 0)
 
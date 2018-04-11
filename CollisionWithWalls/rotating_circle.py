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
        self.inertia = 0.5 * self.mass * self.radius * self.radius
        self.angle = angle
        self.ang_vel = angvel
        self.ang_mom = self.inertia * self.ang_vel
        self.linecolor = linecolor
        self.torque = 0
        
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
        
        self.ang_mom += self.torque * dt
        self.update_ang_vel()
        
    def set_vel(self, vel):
        self.vel.copy_in(vel)
        self.mom.copy_in(self.vel*self.mass)

    def update_vel(self):
        self.vel.copy_in(self.mom/self.mass)
        
    def update_ang_vel(self):
        self.ang_vel = self.ang_mom / self.inertia

    def update_pos(self, dt):
        self.pos += self.vel*dt
        
        self.angle += self.ang_vel * dt
        
    def impulse(self, new_impulse, point_of_impulse):
        self.mom += new_impulse
        self.update_vel()
        self.ang_mom += (point_of_impulse - self.pos).cross(new_impulse)
        self.update_ang_vel()
        
    def update(self, dt):
        self.update_mom(dt)
        self.update_pos(dt)
    
    def draw(self, target, coords):
        super().draw(target, coords)
        endpoint = self.pos + Vec2d(self.radius * math.cos(self.angle), self.radius * math.sin(self.angle))
        pygame.draw.line(target, self.linecolor, coords.pos_to_screen(self.pos).int(), 
                         coords.pos_to_screen(endpoint).int())
        
        
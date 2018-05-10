# -*- coding: utf-8 -*-

import pygame
from vec2d import Vec2d
from Interpolation import Interpolation
from KinematicObject import KinematicObject

class Flipper(KinematicObject):
  def __init__(self, pos, points, color, angle=0):
    #                 pos, vel,     density, points, color, e=0, mu=0, angle=0, angvel=0
    super().__init__(pos, Vec2d(0, 0), 1.0, points, color, 0, 0, angle, 0)
    self.type = "kinematic"
    self.can_interact = True
    
    self.flip_duration = 2.0
    self.flip_angle = 45
        
  def flip(self):
    initial_val = self.angle
    final_val = self.angle + self.flip_angle
    return Interpolation(Interpolation.linear_equation, initial_val, final_val, 
                         self.flip_callback, self.flip_on_complete, self.flip_duration)
    
  def flip_callback(self, val):
    self.angle = val
    
  def flip_on_complete(self):
    print("Flip complete")
    
    
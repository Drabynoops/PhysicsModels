# -*- coding: utf-8 -*-



import pygame
from vec2d import Vec2d
from CollisionObject import CollisionObject
from PhysicsObject import PhysicsObject
from KinematicObject import KinematicObject

class Trigger(KinematicObject):
  def __init__(self, pos, points, color, angle=0):
    #                 pos, vel,     density, points, color, e=0, mu=0, angle=0, angvel=0
    super().__init__(pos, Vec2d(0, 0), 0.0, points, color, 0, 0, angle, 0)
    self.type = "trigger"
    self.callback_func = None
    self.active = True

  def callback(self):
    if self.callback_func != None:
      self.callback_func()
    
  def set_callback(self, callback):
    self.callback = callback
    
  def test_callback(self):
    print("In the trigger!")
    
 
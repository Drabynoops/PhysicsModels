# -*- coding: utf-8 -*-
"""
Created on Wed May  9 09:31:59 2018

@author: Student
"""

import pygame
from vec2d import Vec2d

def update_interpolation_list(interp_list, dt):
  for interp in interp_list:
    interp.update(dt)
  clean_interpolation_list(interp_list) # Clean after updating

def clean_interpolation_list(interp_list):
  i = 0
  while i != len(interp_list):
    # Remove interpolation if it is completed
    if interp_list[i].complete:
      interp_list.remove(interp_list[i])
      i -= 1
    i += 1

def test_callback(val):
  print("Val:", val)

class Interpolation:
  def __init__(self, interpolation_equation, initial_val, final_val, callback, on_complete_callback, duration=1.0):
    self.dt = 0.0001
    self.elapsed_time = 0.0
    self.percentage_complete = 0.0
    
    self.equation = interpolation_equation
    self.duration = duration
    
    self.interp_data_type = -1 # -1 = invalid, 0 = number, 1 = Vec2d
    if isinstance(initial_val, (int, float, complex)):
      self.interp_data_type = 0
    elif isinstance(initial_val, Vec2d):
      self.interp_data_type = 1
    
    self.initial_val = initial_val
    self.final_val = final_val
    self.callback = callback
    self.on_complete_callback = on_complete_callback
    
    self.complete = False
  
  def update(self, dt):
    self.dt = dt
    self.elapsed_time += dt

    if self.complete == False:
      self.percentage_complete = (self.elapsed_time / self.duration)
      
      # Perform easing
      calculated_val = 0
      if self.interp_data_type == 0:
        calculated_val = self.EasedNumber()
      elif self.interp_data_type == 1:
        calculated_val = self.EasedVector()
      
      self.callback(calculated_val)
      
      # When completed interpolation...
      if self.percentage_complete >= 1.0:
        self.percentage_complete = 1.0
        self.callback(self.final_val)
        self.complete = True
        
        # If there is an on_complete_callback, call it
        if self.on_complete_callback != None:
          self.on_complete_callback()
      
    else:
      self.callback(self.final_val)

  def EasedVector(self):
    t = self.elapsed_time
    calculated_vel = Vec2d(0, 0)
    calculated_vel.x = self.equation(t, self.initial_val.x, self.final_val.x - self.initial_val.x, self.duration)
    calculated_vel.y = self.equation(t, self.initial_val.y, self.final_val.y - self.initial_val.y, self.duration)
    return calculated_vel
    
  def EasedNumber(self):
    t = self.elapsed_time
    return self.equation(t, self.initial_val, self.final_val - self.initial_val, self.duration)
 
  
  # ----------------------------
  # INTERPOLATION EQUATIONS     \
  # -----------------------------
  #   > t = current time of the tween
  #   > b = beginning value of the property
  #   > c = change between the beginning and the destination value of the property
  #   > d = total time of the tween
  
  @staticmethod
  def linear_equation(t, b, c, d):
    return (c * t) / (d + b)
  
  @staticmethod
  def in_cubic(t, b, c, d):
    t /= d
    tc = t * t * t
    return b + c * (tc)
  
  @staticmethod
  def out_cubic(t, b, c, d):
    t /= d
    ts = t * t
    tc = ts * t
    return b + c * (tc + -3 * ts + 3 * t)

  @staticmethod
  def in_out_cubic(t, b, c, d):
    t /= d
    ts = t * t
    tc = ts * t
    return b + c * (-2 * tc + 3 * ts)

  @staticmethod
  def out_in_cubic(t, b, c, d):
    t /= d
    ts = t * t
    tc = ts * t
    return b + c * (4 * tc + -6 * ts + 3 * t)
  
  @staticmethod
  def in_elastic_big(t, b, c, d):
    t /= d
    ts = t * t
    tc = ts * t
    return b + c * (56 * tc * ts + -105 * ts * ts + 60 * tc + -10 * ts)
  
  @staticmethod
  def out_elastic_big(t, b, c, d):
    t /= d
    ts = t * t
    tc = ts * t
    return b + c * (56 * tc * ts + -175 * ts * ts + 200 * tc + -100 * ts + 20 * t)
  
  @staticmethod
  def bounce(t, b, c, d):
    t2 = t / d
    if (t < d):
      if (t2 < (1 / 2.75)):
        return c * (7.5625 * t2 * t2) + b
      elif (t2 < (2 / 2.75)):
        t2 -= (1.5 / 2.75)
        return c * (7.5625 * t2 * t2 + 0.75) + b
      elif (t2 < (2.5 / 2.75)):
        t2 -= (2.25 / 2.75)
        return c * (7.5625 * t2 * t2 + 0.9375) + b
      else:
        t2 -= (2.625 / 2.75)
        return c * (7.5625 * t2 * t2 + 0.984375) + b
    else:
        return c + b
  
  
  
  
  
  
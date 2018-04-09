# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:38:47 2018

@author: Student
"""

class RotatingCircle(Circle):
    def __init__(pos, vel, mass, radius, color, angle=0, angvel=0, linecolor):
        super().__init__(pos, vel, mass, radius, color)
        self.angle = angle
        
        
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 22:14:05 2018

@author: Keenan Barber
"""

from vec2d import Vec2d

class TextElement:
    def __init__(self, font, pos, textStr, offsetX=0.5, offsetY=0.5, color=(0,0,0)):
        self.pos = pos
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.font = font
        self.color = color
        self.text = font.render(textStr,True,color) # Creates the text (text, anti-aliased, color)
            
    def setText(self, textStr):
        self.text = self.font.render(textStr,True,self.color)
        
    def setAnchor(self, x, y): # x=(0-1), y=(0-1)
        self.offsetX = x
        self.offsetY = y
    
    def draw(self, screen, coords):
        rect = self.text.get_rect()
        offsetPos = Vec2d(
            self.pos.x - coords.scalar_to_coords(self.offsetX * rect.width), 
            self.pos.y + coords.scalar_to_coords(self.offsetY * rect.height)
        )
        screen.blit(self.text, coords.pos_to_screen(offsetPos).int()) # (textObj, location)

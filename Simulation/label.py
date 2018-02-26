# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:10:02 2018

@author: Keenan Barber, Brendan Bard
"""

import pygame
from color import Color

class Label:
    # Constructor
    def __init__(self, labelText, fontSize, vec):
        self.position = vec
        self.labelText = labelText
        self.fontSize = fontSize
        self.font = pygame.font.SysFont('Calibri', self.fontSize, True, False) # Gets a font (font, size, bold, italics)
        self.text = self.font.render(self.labelText, True, Color.BLUE) # Creates the text (text, anti-aliased, color)
        
    def draw(self, screen):           
        offsetX = self.text.get_rect().width / 2
        offsetY = self.text.get_rect().height / 2
        screen.blit(self.text, [self.position.x - offsetX, self.position.y - offsetY]) # Puts image of text on screen (textObj, location)
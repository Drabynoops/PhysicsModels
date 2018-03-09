# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:10:02 2018

@author: Keenan Barber, Brendan Bard
"""

import pygame
from color import Color
from enum import Enum
from vec2d import Vec2d

# Global variables to set some basic details about the buttons
BUTTON_INNER_BORDER_THICKNESS = 4
BUTTON_OUTER_BORDER_THICKNESS = 2


""" ANCHOR ENUM --------------------------------------

    TOP_LEFT            TOP            TOP_RIGHT
               +---------+---------+
               |         |         |
    LEFT       +-------CENTER------+   RIGHT
               |         |         |
               +---------+---------+
    BOTTOM_LEFT        BOTTOM          BOTTOM_RIGHT

"""
class Anchor(Enum):
    TOP_LEFT = 1
    TOP = 2
    TOP_RIGHT = 3
    LEFT = 4
    CENTER = 5
    RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM = 8 
    BOTTOM_RIGHT = 9
    
# Returns a vector to get the offset required for setting a position
def get_anchor_offset(anchor, width, height):
    if anchor == Anchor.TOP_LEFT:
        return Vec2d(0, 0)
    elif anchor == Anchor.TOP:
        return Vec2d(width / 2, 0)
    elif anchor == Anchor.TOP_RIGHT:
        return Vec2d(width, 0)
    elif anchor == Anchor.LEFT:
        return Vec2d(0, height / 2)
    elif anchor == Anchor.CENTER:
        return Vec2d(width / 2, height / 2)
    elif anchor == Anchor.RIGHT:
        return Vec2d(width, height / 2)
    elif anchor == Anchor.BOTTOM_LEFT:
        return Vec2d(0, height)
    elif anchor == Anchor.BOTTOM:
        return Vec2d(width / 2, height)
    elif anchor == Anchor.BOTTOM_RIGHT:
        return Vec2d(width, height)



# The UIButton class is used to create buttons on a given screen
class UIButton:
    # Constructor
    def __init__(self, button_text, font_size, anchor, pos, size):     
        self.pressed = False
        self.press_functions = []
        
        # Size Variables
        self.width = size.x
        self.height = size.y
        
        # Position Variables
        self.position = pos
        self.anchor = anchor
        self.anchor_offset = get_anchor_offset(anchor, self.width, self.height)
        
        # Text Variables
        self.button_text = button_text
        self.font = pygame.font.SysFont('Calibri', font_size, True, False) # Gets a font (font, size, bold, italics)
        
        # Button Colors
        self.button_color_selected = Color.WHITE
        self.text_color_selected = Color.BLACK
        self.button_color_unselected = Color.BLACK
        self.text_color_unselected = Color.WHITE
        self.outer_border_color = Color.WHITE
        
    # Used to set basic details about the button
    def set_details(self, font_size, anchor_enum):
        self.font = pygame.font.SysFont('Calibri', font_size, True, False)
        self.anchor = anchor_enum
        self.anchor_offset = get_anchor_offset(anchor_enum, self.width, self.height)
        
    # Sets the colors of the button and its text
    def set_colors(self, button_color_selected, button_color_unselected, text_color_selected, text_color_unselected):
        self.button_color_selected = button_color_selected
        self.outer_border_color = button_color_selected
        self.text_color_selected = text_color_selected
        self.button_color_unselected = button_color_unselected
        self.text_color_unselected = text_color_unselected

    # Call all on press functions that have been added to the button        
    def press_event(self):
        for func in self.press_functions:
            func()
    
    # Adds a new function to be called when pressed 
    def add_event(self, func):
        self.press_functions.append(func)
        
    # Draws the button as either pressed, highlighted, or neither
    def draw(self, screen):    
        if self.mouse_over() or self.pressed == True:
            # Button Background
            pygame.draw.rect(screen, self.outer_border_color, (self.position.x - self.anchor_offset.x, self.position.y - self.anchor_offset.y, self.width, self.height), BUTTON_OUTER_BORDER_THICKNESS)
            pygame.draw.rect(screen, self.button_color_selected, 
                 (self.position.x - self.anchor_offset.x + BUTTON_OUTER_BORDER_THICKNESS + BUTTON_INNER_BORDER_THICKNESS, 
                 self.position.y - self.anchor_offset.y + BUTTON_OUTER_BORDER_THICKNESS + BUTTON_INNER_BORDER_THICKNESS, 
                 self.width - (2 * BUTTON_OUTER_BORDER_THICKNESS) - (2 * BUTTON_INNER_BORDER_THICKNESS), 
                 self.height - (2 * BUTTON_OUTER_BORDER_THICKNESS) - (2 * BUTTON_INNER_BORDER_THICKNESS)))
    
            # Draws the text on the button
            text = self.font.render(self.button_text, True, self.text_color_selected) # Creates the text (text, anti-aliased, color)
            text_offset_x = (text.get_rect().width / 2) - (self.width / 2) + self.anchor_offset.x
            text_offset_y = (text.get_rect().height / 2) - (self.height / 2) + self.anchor_offset.y
            screen.blit(text, [self.position.x - text_offset_x, self.position.y - text_offset_y]) # Puts image of text on screen (textObj, location)
            
        else:
            # Button Background
            pygame.draw.rect(screen, self.outer_border_color, (self.position.x - self.anchor_offset.x, self.position.y - self.anchor_offset.y, self.width, self.height), BUTTON_OUTER_BORDER_THICKNESS)
            pygame.draw.rect(screen, self.button_color_unselected, 
                 (self.position.x - self.anchor_offset.x + BUTTON_OUTER_BORDER_THICKNESS + BUTTON_INNER_BORDER_THICKNESS, 
                 self.position.y - self.anchor_offset.y + BUTTON_OUTER_BORDER_THICKNESS + BUTTON_INNER_BORDER_THICKNESS, 
                 self.width - (2 * BUTTON_OUTER_BORDER_THICKNESS) - (2 * BUTTON_INNER_BORDER_THICKNESS), 
                 self.height - (2 * BUTTON_OUTER_BORDER_THICKNESS) - (2 * BUTTON_INNER_BORDER_THICKNESS)))

            # Draws the text on the button
            text = self.font.render(self.button_text, True, self.text_color_unselected) # Creates the text (text, anti-aliased, color)
            text_offset_x = (text.get_rect().width / 2) - (self.width / 2) + self.anchor_offset.x
            text_offset_y = (text.get_rect().height / 2) - (self.height / 2) + self.anchor_offset.y
            screen.blit(text, [self.position.x - text_offset_x, self.position.y - text_offset_y]) # Puts image of text on screen (textObj, location)
        
    # Returns the rectangle surrounding the button
    def get_rect(self):
        return pygame.Rect(self.position.x - self.anchor_offset.x, self.position.y - self.anchor_offset.y, self.width, self.height)
    
    # Returns whether or not the mouse is over the button
    def mouse_over(self):
        self.mouseOver = self.get_rect().collidepoint(pygame.mouse.get_pos())
        return self.mouseOver
    
    
# The UILabel class is used to create labels / text on a given screen
class UILabel:
    # Constructor
    def __init__(self, label_text, font_size, color, anchor, pos):
        # Default Font
        self.font = pygame.font.SysFont('Calibri', font_size, True, False) # Gets a font (font, size, bold, italics)
        
        # Text Variables
        self.text_color = color
        self.label_text = label_text
        self.text = self.font.render(self.label_text, True, self.text_color) # Creates the text (text, anti-aliased, color)
        
        # Size Variables
        self.width = self.text.get_rect().width
        self.height = self.text.get_rect().height
        
        # Position Variables
        self.position = pos
        self.anchor = anchor
        self.anchor_offset = get_anchor_offset(anchor, self.width, self.height)
        
    # Sets details about the text like the font size and the anchor point
    def set_details(self, font_size, anchor_enum):
        self.font = pygame.font.SysFont('Calibri', font_size, True, False)
        self.text = self.font.render(self.label_text, True, self.text_color) # Creates the text (text, anti-aliased, color)
        
        self.anchor = anchor_enum
        self.anchor_offset = get_anchor_offset(anchor_enum, self.width, self.height)
        
    def set_text(self, str):
        self.label_text = str
        self.text = self.font.render(self.label_text, True, self.text_color) # Creates the text (text, anti-aliased, color)
        
    # Sets the color of the text
    def set_color(self, text_color):
        self.text_color = text_color
    
    # Draws the label to the provided screen
    def draw(self, screen):    
            #pygame.draw.rect(screen, Color.RED, (self.position.x - self.anchor_offset.x, self.position.y - self.anchor_offset.y, self.width, self.height), BUTTON_OUTER_BORDER_THICKNESS)
            screen.blit(self.text, [self.position.x - self.anchor_offset.x, self.position.y - self.anchor_offset.y]) # Puts image of text on screen (textObj, location)
        
    # Gets the rectangle surrounding the text
    def get_rect(self):
        return pygame.Rect(self.position.x - self.anchor_offset.x, self.position.y - self.anchor_offset.y, self.width, self.height)

    
    
# The UIButtonGroup class is used to create a group of buttons where only one 
# can be selected at a time. This will behave like a radio button group. 
class UIButtonGroup:
    # Constructor
    def __init__(self):
        self.buttons = []
        self.active_button = None
        self.previous_button = None
    
    # Adds a new button to the group (if first button, set it as active by default)
    def add(self, ui_button):
        self.buttons.append(ui_button)
        if(len(self.buttons) == 1):
            self.active_button = ui_button
    
    # Finds the button that is under the mouse
    def get_button_under_mouse(self):
        for button in self.buttons:
            if button.mouse_over():
                return button
        return None
    
    # Changes the currently selected button
    def set_active(self, button):
        self.previous_button = self.active_button
        if self.previous_button != None:
            self.previous_button.pressed = False
        
        self.active_button = button
        if len(self.buttons) != 1:
            self.active_button.pressed = True
            
    def get_active_button_text(self):
        return self.active_button.button_text
        
    # Loops through all of the buttons and calls the draw function on them
    def draw(self, screen):        
        for button in self.buttons:
            button.draw(screen)
        
    # Checks to see if there is a new button that is being selected
    # (Supposed to be called on a mouse down event)
    def check_mouse_down(self):
        highlighted_button = self.get_button_under_mouse()
        if highlighted_button != None:
            self.set_active(highlighted_button)
            self.active_button.press_event()
            return True
        else:
            return False








    
    
    
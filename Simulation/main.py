# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:50:00 2018

@author: Keenan Barber, Brendan Bard
"""

import pygame
import random

from color import Color
from vec2d import Vec2d
from particle_system import Particle, System
from ui_elements import UIButton, UILabel, UIButtonGroup, Anchor

class Simulation:

    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width,height])
        self.background_color = Color.BLACK

        self.draw_screen = self.screen.copy()
        self.draw_screen.fill(Color.BLACK)
        self.end_screen = None
        
        self.dt = 0.001
        self.state = self.play # The game state
        self.done = False
        
        self.system = System

        # --- UI Elements -------------------
        self.initialize_ui()

        # Create the sprite groups
        self.game_objects = pygame.sprite.Group()

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        
    def execute_game_loop(self):
        # -------- Main Program Loop -----------\
        while not self.done:
            self.state()
            

        pygame.quit()
    
    def play(self):
        # --- Main event loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                self.done = True
            elif event.type == pygame.KEYDOWN:
                print("Key down")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.action_button_group.update_selection()
                self.play_state_button_group.update_selection()
                
        # --- Drawing code should go here
        # First, clear the screen
        self.screen.fill(self.background_color) 
        
        # --- Draw UI Elements
        self.title.draw(self.screen)
        self.action_button_group.draw(self.screen)
        self.play_state_button_group.draw(self.screen)
        self.center_view_button.draw(self.screen)
        self.author_label.draw(self.screen)

        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        self.clock.tick(60)
        
    def run(self):
        pass
    
    # Used to initialize the UI elements
    def initialize_ui(self):
        # UI Settings
        start_from_left = 10
        start_from_top = 10     
        button_height = 30
        button_spacing = 10
        
        # --- UI Labels -------------------
        self.title = UILabel("Gravity Simulation", 30, Color.WHITE, Anchor.TOP_LEFT, Vec2d(start_from_left, start_from_top))
        self.author_label = UILabel("Authors: Keenan Barber, Brendan Bard", 16, Color.WHITE, Anchor.BOTTOM_LEFT, Vec2d(start_from_left, self.height))
        
        # --- UI Buttons -------------------
        
        # Pointer Button (In Action Group)
        self.pointer_button = UIButton("Pointer", 16, Anchor.TOP_LEFT, 
            Vec2d(start_from_left, start_from_top + self.title.height + (0 * button_height) + (1 * button_spacing)),    # Position
            Vec2d(150, button_height))                                                                                  # Size
        self.pointer_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                              # Button Colors
        
        # Add Particle Button (In Action Group)
        self.add_button = UIButton("Add Particle", 16, Anchor.TOP_LEFT, 
            Vec2d(start_from_left, start_from_top + self.title.height + (1 * button_height) + (2 * button_spacing)),    # Position
            Vec2d(150, button_height))                                                                                  # Size
        self.add_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                                  # Button Colors
        
        # Remove Particle Button (In Action Group)
        self.remove_button = UIButton("Remove Particle", 16, Anchor.TOP_LEFT, 
            Vec2d(start_from_left, start_from_top + self.title.height + (2 * button_height) + (3 * button_spacing)),    # Position
            Vec2d(150, button_height))                                                                                  # Size
        self.remove_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                               # Button Colors
        
        # Play Button (In Play State Group)
        self.play_button = UIButton("Play", 16, Anchor.BOTTOM_LEFT, 
            Vec2d(start_from_left, self.height - self.author_label.height - button_spacing),                            # Position
            Vec2d(70, button_height))                                                                                   # Size
        self.play_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                                 # Button Colors
        
        # Pause Button (In Play State Group)
        self.pause_button = UIButton("Pause", 16, Anchor.BOTTOM_LEFT, 
            Vec2d(start_from_left + button_spacing + 70, self.height - self.author_label.height - button_spacing),      # Position
            Vec2d(70, button_height))                                                                                   # Size
        self.pause_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                                # Button Colors
        
        # Center View Button
        self.center_view_button = UIButton("Center View  [0]", 16, Anchor.BOTTOM_LEFT, 
            Vec2d(start_from_left, self.height - self.author_label.height - button_height - (2 * button_spacing)),      # Position
            Vec2d(150, button_height))                                                                                  # Size
        self.center_view_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                          # Button Colors
        
        # --- UI Button Groups -------------------
        
        # Group to hold the main action ability buttons
        self.action_button_group = UIButtonGroup()
        self.action_button_group.add(self.pointer_button)
        self.action_button_group.add(self.add_button)
        self.action_button_group.add(self.remove_button)
        self.action_button_group.set_active(self.pointer_button)
        
        # Group to hold the play and pause buttons
        self.play_state_button_group = UIButtonGroup()
        self.play_state_button_group.add(self.play_button)
        self.play_state_button_group.add(self.pause_button)
        self.play_state_button_group.set_active(self.play_button)

def main():
    sim = Simulation(800, 600)
    sim.execute_game_loop()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 

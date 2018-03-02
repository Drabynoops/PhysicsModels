# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:50:00 2018

@author: Keenan Barber, Brendan Bard
"""

import pygame
import random
from enum import Enum

from color import Color
from vec2d import Vec2d
from particle_system import Particle, System
from ui_elements import UIButton, UILabel, UIButtonGroup, Anchor

class InteractionType(Enum):
    POINTER = 1, 
    ADD_PARTICLE = 2, 
    REMOVE_PARTICLE = 3

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
        
        self.use_pointer()
        
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
                # Checks to see if any groups have any buttons highlighted
                if self.action_group.check_mouse_down() or self.time_state_group.check_mouse_down() or self.view_group.check_mouse_down():
                    print("Clicked a button!")
                else: 
                    print("Didn't click a button!")
                
        # --- Drawing code should go here
        # First, clear the screen
        self.screen.fill(self.background_color) 
        
        # --- Draw UI Elements
        self.title.draw(self.screen)
        self.action_group.draw(self.screen)
        self.time_state_group.draw(self.screen)
        self.view_group.draw(self.screen)
        self.author_label.draw(self.screen)

        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        self.clock.tick(60)
        
    def run(self):
        pass
    
    # --- Events to be called by buttons! 
    def use_pointer(self):
        print("Using the pointer tool...")
        self.interaction_type = InteractionType.POINTER
        
    def use_add(self):
        print("Using the add tool...")
        self.interaction_type = InteractionType.ADD_PARTICLE
        
    def use_remove(self):
        print("Using the remove tool...")
        self.interaction_type = InteractionType.REMOVE_PARTICLE
        
    def center_view(self):
        print("Centering view...")
        
    def play_sim(self):
        print("Playing the simulation...")
        
    def pause_sim(self):
        print("Pausing the simulation...")
    
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
        self.pointer_button.add_event(self.use_pointer)                                                                 # Add event
        
        # Add Particle Button (In Action Group)
        self.add_button = UIButton("Add Particle", 16, Anchor.TOP_LEFT, 
            Vec2d(start_from_left, start_from_top + self.title.height + (1 * button_height) + (2 * button_spacing)),    # Position
            Vec2d(150, button_height))                                                                                  # Size
        self.add_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                                  # Button Colors
        self.add_button.add_event(self.use_add)                                                                         # Add event
        
        # Remove Particle Button (In Action Group)
        self.remove_button = UIButton("Remove Particle", 16, Anchor.TOP_LEFT, 
            Vec2d(start_from_left, start_from_top + self.title.height + (2 * button_height) + (3 * button_spacing)),    # Position
            Vec2d(150, button_height))                                                                                  # Size
        self.remove_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                               # Button Colors
        self.remove_button.add_event(self.use_remove)                                                                   # Add event
        
        # Play Button (In Play State Group)
        self.play_button = UIButton("Play", 16, Anchor.BOTTOM_LEFT, 
            Vec2d(start_from_left, self.height - self.author_label.height - button_spacing),                            # Position
            Vec2d(70, button_height))                                                                                   # Size
        self.play_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                                 # Button Colors
        self.play_button.add_event(self.play_sim)                                                                    # Add event
        
        # Pause Button (In Play State Group)
        self.pause_button = UIButton("Pause", 16, Anchor.BOTTOM_LEFT, 
            Vec2d(start_from_left + button_spacing + 70, self.height - self.author_label.height - button_spacing),      # Position
            Vec2d(70, button_height))                                                                                   # Size
        self.pause_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                                # Button Colors
        self.pause_button.add_event(self.pause_sim)                                                                   # Add event
        
        # Center View Button
        self.center_view_button = UIButton("Center View  [0]", 16, Anchor.BOTTOM_LEFT, 
            Vec2d(start_from_left, self.height - self.author_label.height - button_height - (2 * button_spacing)),      # Position
            Vec2d(150, button_height))                                                                                  # Size
        self.center_view_button.set_colors(Color.WHITE, Color.BLACK, Color.BLACK, Color.WHITE)                          # Button Colors
        self.center_view_button.add_event(self.center_view)                                                             # Add event
        
        # --- UI Button Groups -------------------
        
        # Group to hold the center view button
        self.view_group = UIButtonGroup()
        self.view_group.add(self.center_view_button)
        self.view_group.set_active(self.center_view_button)
        
        # Group to hold the main action ability buttons
        self.action_group = UIButtonGroup()
        self.action_group.add(self.pointer_button)
        self.action_group.add(self.add_button)
        self.action_group.add(self.remove_button)
        self.action_group.set_active(self.pointer_button)
        
        # Group to hold the play and pause buttons
        self.time_state_group = UIButtonGroup()
        self.time_state_group.add(self.play_button)
        self.time_state_group.add(self.pause_button)
        self.time_state_group.set_active(self.play_button)

def main():
    sim = Simulation(800, 600)
    sim.execute_game_loop()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 

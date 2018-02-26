# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:50:00 2018

@author: Keenan Barber, Brendan Bard
"""

import pygame
import random

from color import Color
from vec2d import Vec2d

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

        # --- Drawing code should go here
        # First, clear the screen
        self.screen.fill(self.background_color) 
        

        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        self.clock.tick(60)
        
    def run(self):
        pass

def main():
    sim = Simulation(800, 600)
    sim.execute_game_loop()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 

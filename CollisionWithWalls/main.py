# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:50:00 2018

@author: Keenan Barber, Brendan Bard
"""

import pygame
import random
from enum import Enum

from coords import Coords
from color import Color, random_color
from vec2d import Vec2d
from particle_system import System   
from circle import Circle
from wall import Wall

class Simulation:

    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width,height])
        
        # Set up coords
        self.screen_center = Vec2d(width/2, height/2)
        self.coords = Coords(self.screen_center.copy(), 1, True)
        self.zoom = 10
        self.coords.zoom_at_coords(Vec2d(0,0), self.zoom) 
        self.zoomed_width = width / self.zoom
        self.zoomed_height = height / self.zoom
        
        self.background_color = Color.BLACK

        self.draw_screen = self.screen.copy()
        self.draw_screen.fill(Color.BLACK)
        self.end_screen = None
        
        self.state = self.play # The game state
        self.paused = False
        self.done = False
        
        self.frame_rate = 60
        self.playback_speed = 1 # 1 is real time, 10 is 10x real speed, etc.
        self.dt = self.playback_speed/self.frame_rate
        
        # Create System with walls
        self.system = System()
        test = 15
        self.system.create_wall(Vec2d(-test, -test), Vec2d(1, 1))
        self.system.create_wall(Vec2d(test, -test), Vec2d(-1, 1))
        
        # Add circles!
        rand_circle_count = 10
        rand_circle_min_radius = 3
        rand_circle_max_radius = 5
        for x in range(0, rand_circle_count):
            rand_radius = random.randint(rand_circle_min_radius,rand_circle_max_radius)
            half_width = self.zoomed_width / 2
            half_height = self.zoomed_height / 2
            rand_pos = Vec2d(random.randint(-half_width, half_width), random.randint(-half_height, half_height))
            
            self.system.create_circle(rand_radius, rand_pos, Vec2d(0, 0))

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        
    def execute_game_loop(self):
        # -------- Main Program Loop -----------\
        while not self.done:
            self.state()

        pygame.quit()
    
    def play(self):
        # --- Main event loop
        mouse_pos = Vec2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                self.done = True
            elif event.type == pygame.KEYDOWN: 
                print("Key down")
                
            # --- MOUSE DOWN ---------
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    
                pass
                    
            # --- MOUSE UP ---------
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:      
                pass

                
        # --- Drawing code should go here
        self.screen.fill(self.background_color) 
        
        # --- Physics goes here
        if not self.paused:
            self.system.update(self.dt)
            pass  

        # --- Draw the system of particles
        self.system.draw(self.screen, self.coords)

        # --- Update the screen with what we've drawn.
        pygame.display.update()
        self.clock.tick(self.frame_rate)
        
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

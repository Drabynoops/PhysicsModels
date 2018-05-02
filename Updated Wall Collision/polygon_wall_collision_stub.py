# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d
from collision_system_functions import game_settings, create_objects, check_collision, resolve_collision, WHITE


def main():
    pygame.init()
 
    # Get all basic game settings
    (screen, coords, zoom, frame_rate, n_per_frame, playback_speed) = game_settings()
    coords.zoom_at_coords(Vec2d(0,0), zoom) 
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Create initial objects to demonstrate
    objects = create_objects()

    # -------- Main Program Loop -----------\
    dt = playback_speed/frame_rate/n_per_frame
    done = False
    paused = True
    max_collisions = 1
    result = []
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
                paused = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                paused = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    done = True
                    paused = True 
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                else:
                    paused = False
        
        if not paused:
            for N in range(n_per_frame):
                # Physics
                # Calculate the force on each object
                for obj in objects:
                    obj.force.zero()
                    obj.force += Vec2d(0,-10) # gravity
           
                # Move each object according to physics
                for obj in objects:
                    obj.update(dt)
                    
                for i in range(max_collisions):
                    collided = False
                    for i1 in range(len(objects)):
                        for i2 in range(i1):
                            if check_collision(objects[i1], objects[i2], result):
                                resolve_collision(result)
                                collided = True
                    if not collided: # if all collisions resolved, then we're done
                        break
 
        # Drawing
        screen.fill(WHITE) # wipe the screen
        for obj in objects:
            obj.draw(screen, coords) # draw object to screen

        # --- Update the screen with what we've drawn.
        pygame.display.update()
        
        # This limits the loop to the specified frame rate
        clock.tick(frame_rate)
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
